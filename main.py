import argparse
import os
import warnings
from datetime import datetime
from pathlib import Path

import pytorch_lightning as pl
import torch
from pytorch_lightning.callbacks import ModelCheckpoint
from transformers import AutoConfig
from transformers import AutoTokenizer

from callbacks import PrintingCallback
from data import DataModule
from helper import get_num, read, read_name, read_file, get_ground_truth, get_next_token_dict, construct_prefix_trie
from models.model import T5Finetuner


def main():
    ## read triples
    train_triples = read(configs, configs.dataset_path, configs.dataset, 'train2id.txt')
    valid_triples = read(configs, configs.dataset_path, configs.dataset, 'valid2id.txt')
    test_triples = read(configs, configs.dataset_path, configs.dataset, 'test2id.txt')
    all_triples = train_triples + valid_triples + test_triples

    ## construct name list
    original_ent_name_list, rel_name_list = read_name(configs, configs.dataset_path, configs.dataset)
    description_list = read_file(configs, configs.dataset_path, configs.dataset, 'entityid2description.txt', 'descrip')
    config = AutoConfig.from_pretrained(configs.pretrained_model)
    tokenizer = AutoTokenizer.from_pretrained(configs.pretrained_model)
    if '<extra_id_0>' not in tokenizer.additional_special_tokens:
        tokenizer = AutoTokenizer.from_pretrained(configs.pretrained_model, additional_special_tokens=['<extra_id_0>', '<extra_id_1>'])
    extra_id_0_tok_id = tokenizer('<extra_id_0>').input_ids[0]
    print()
    print("----------------------------------------------------------------------------------")
    print(f" - pretrained_model.model_type: {config.model_type}")
    print(f" - tokenizer.additional_special_tokens: {tokenizer.additional_special_tokens}")
    print(f" - extra_id_0_tok_id: {extra_id_0_tok_id}")
    print("----------------------------------------------------------------------------------")
    print()
    print('tokenizing entities...')
    src_description_list = tokenizer.batch_decode([descrip[:-1] for descrip in tokenizer(description_list, max_length=configs.src_descrip_max_length, truncation=True).input_ids])
    tgt_description_list = tokenizer.batch_decode([descrip[:-1] for descrip in tokenizer(description_list, max_length=configs.tgt_descrip_max_length, truncation=True).input_ids])

    ## construct prefix trie
    # ent_token_ids_in_trie .type: list(list(ids))
    ent_token_ids_in_trie = tokenizer(['<extra_id_0>' + ent_name + '<extra_id_1>' for ent_name in original_ent_name_list], max_length=configs.train_tgt_max_length, truncation=True).input_ids

    if configs.tgt_descrip_max_length > 0:
        ent_token_ids_in_trie_with_descrip = tokenizer(['<extra_id_0>' + ent_name + '[' + tgt_description_list[i] + ']' + '<extra_id_1>' for i, ent_name in enumerate(original_ent_name_list)], max_length=configs.train_tgt_max_length, truncation=True).input_ids
        prefix_trie = construct_prefix_trie(ent_token_ids_in_trie_with_descrip)
        neg_candidate_mask, next_token_dict = get_next_token_dict(configs, ent_token_ids_in_trie_with_descrip, prefix_trie, extra_id_0_token_id=extra_id_0_tok_id)
    else:
        prefix_trie = construct_prefix_trie(ent_token_ids_in_trie)
        neg_candidate_mask, next_token_dict = get_next_token_dict(configs, ent_token_ids_in_trie, prefix_trie, extra_id_0_token_id=extra_id_0_tok_id)
    ent_name_list = tokenizer.batch_decode([tokens[1:-2] for tokens in ent_token_ids_in_trie])
    name_list_dict = {
        'original_ent_name_list': original_ent_name_list,
        'ent_name_list': ent_name_list,
        'rel_name_list': rel_name_list,
        'src_description_list': src_description_list,
        'tgt_description_list': tgt_description_list
    }

    prefix_trie_dict = {
        'prefix_trie': prefix_trie,
        'ent_token_ids_in_trie': ent_token_ids_in_trie,
        'neg_candidate_mask': neg_candidate_mask,
        'next_token_dict': next_token_dict
    }
    if configs.tgt_descrip_max_length > 0:
        prefix_trie_dict['ent_token_ids_in_trie_with_descrip'] = ent_token_ids_in_trie_with_descrip

    ## construct ground truth dictionary
    # ground truth .shape: dict, example: {hr_str_key1: [t_id11, t_id12, ...], (hr_str_key2: [t_id21, t_id22, ...], ...}
    train_tail_ground_truth, train_head_ground_truth = get_ground_truth(configs, train_triples)
    all_tail_ground_truth, all_head_ground_truth = get_ground_truth(configs, all_triples)

    ground_truth_dict = {
        'train_tail_ground_truth': train_tail_ground_truth,
        'train_head_ground_truth': train_head_ground_truth,
        'all_tail_ground_truth': all_tail_ground_truth,
        'all_head_ground_truth': all_head_ground_truth,
    }

    datamodule = DataModule(configs, train_triples, valid_triples, test_triples, name_list_dict, prefix_trie_dict, ground_truth_dict)
    print('datamodule construction done.', flush=True)

    print()
    print("----------------------------------------------------------------------------------")
    print(f" * pl.Trainer(accelerator={configs.accelerator}, precision={configs.precision}, max_epochs={configs.epochs}, every_n_epoch={configs.check_every_n_epochs})")
    print("----------------------------------------------------------------------------------")
    print()
    checkpoint_callback = ModelCheckpoint(
        dirpath=configs.save_dir,
        filename=configs.dataset + '-{epoch:03d}-{' + 'val_mrr' + ':.4f}',
        every_n_epochs=configs.check_every_n_epochs,
        save_top_k=5,
        monitor='val_mrr',
        mode='max',
    )
    trainer = pl.Trainer(
        devices=1,
        precision=configs.precision,
        accelerator=configs.accelerator,
        max_epochs=configs.epochs,
        check_val_every_n_epoch=configs.check_every_n_epochs,
        accumulate_grad_batches=configs.grad_accumulate,
        num_sanity_val_steps=0,
        enable_progress_bar=True,
        logger=False,
        callbacks=[
            checkpoint_callback,
            PrintingCallback(),
        ],
    )
    kw_args = {
        'ground_truth_dict': ground_truth_dict,
        'name_list_dict': name_list_dict,
        'prefix_trie_dict': prefix_trie_dict
    }

    if configs.model_path == '':
        model = T5Finetuner(configs, **kw_args)
        print('model construction done.', flush=True)
        trainer.fit(model, datamodule)
        model_path = checkpoint_callback.best_model_path
    else:
        model_path = configs.model_path
    print(f'model_path: [{model_path}]', flush=True)
    if model_path:
        model = T5Finetuner.load_from_checkpoint(model_path, strict=False, configs=configs, **kw_args)
        trainer.test(model, dataloaders=datamodule)


if __name__ == '__main__':
    warnings.filterwarnings('ignore', category=DeprecationWarning)
    parser = argparse.ArgumentParser()

    parser.add_argument('-dataset_path', type=str, default='./data/processed')
    parser.add_argument('-dataset', dest='dataset', default='WN18RR', help='Dataset to use, default: WN18RR')
    parser.add_argument('-model', default='T5Finetuner', help='Model Name')
    parser.add_argument('-precision', type=str, default='32', help='Floating point precision')
    parser.add_argument('-accelerator', type=str, default='gpu', help='Type of training accelerator')
    parser.add_argument('-seed', dest='seed', default=41504, type=int, help='Seed for randomization')
    parser.add_argument('-num_workers', type=int, default=12, help='Number of processes to construct batches')
    parser.add_argument('-save_dir', type=str, default='', help='')

    parser.add_argument('-pretrained_model', type=str, default='t5-base', help='')
    parser.add_argument('-batch_size', default=8, type=int, help='Batch size of train set')
    parser.add_argument('-val_batch_size', default=4, type=int, help='Batch size of validation/test set')
    parser.add_argument('-grad_accumulate', default=1, type=int, help='Accumulates grads every k batches')
    parser.add_argument('-num_beams', default=40, type=int, help='Number of samples from beam search')
    parser.add_argument('-num_beam_groups', default=1, type=int, help='')
    parser.add_argument('-src_max_length', default=512, type=int, help='')
    parser.add_argument('-train_tgt_max_length', default=512, type=int, help='')
    parser.add_argument('-eval_tgt_max_length', default=90, type=int, help='')
    parser.add_argument('-epoch', dest='epochs', type=int, default=50, help='Number of epochs')
    parser.add_argument('-lr', type=float, default=0.001, help='Starting Learning Rate')
    parser.add_argument('-diversity_penalty', default=0., type=float, help='')

    parser.add_argument('-model_path', dest='model_path', default='', help='The path for reloading models')
    parser.add_argument('-optim', default='Adam', type=str, help='')
    parser.add_argument('-decoder', type=str, default='beam_search', help='[beam_search, do_sample, beam_sample_search, diverse_beam_search]')
    parser.add_argument('-log_text', action='store_true', help='')
    parser.add_argument('-use_prefix_search', action='store_true', help='')
    parser.add_argument('-src_descrip_max_length', default=0, type=int, help='')
    parser.add_argument('-tgt_descrip_max_length', default=0, type=int, help='')
    parser.add_argument('-use_soft_prompt', action='store_true', help='')
    parser.add_argument('-use_rel_prompt_emb', action='store_true', help='')
    parser.add_argument('-check_every_n_epochs', default=3, type=int, help='')
    parser.add_argument('-seq_dropout', default=0., type=float, help='')
    parser.add_argument('-temporal', action='store_true', help='')
    configs = parser.parse_args()
    n_ent = get_num(configs.dataset_path, configs.dataset, 'entity')
    n_rel = get_num(configs.dataset_path, configs.dataset, 'relation')
    configs.n_ent = n_ent
    configs.n_rel = n_rel
    configs.vocab_size = AutoConfig.from_pretrained(configs.pretrained_model).vocab_size
    configs.model_dim = AutoConfig.from_pretrained(configs.pretrained_model).d_model
    if configs.save_dir == '':
        configs.save_dir = os.path.join('./checkpoint',
                                        '='.join([
                                            configs.dataset,
                                            Path(configs.pretrained_model).name,
                                            datetime.now().strftime('%m%d.%H%M%S')
                                        ]))
    os.makedirs(configs.save_dir, exist_ok=True)
    print(configs, flush=True)

    pl.seed_everything(configs.seed)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True
    torch.set_printoptions(profile='full')
    torch.set_float32_matmul_precision('high')
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    main()
