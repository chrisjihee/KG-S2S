python3 main.py -dataset 'WN18RR' \
                -src_descrip_max_length 40 \
                -tgt_descrip_max_length 10 \
                -use_soft_prompt \
                -use_rel_prompt_emb \
                -num_beams 40 \
                -eval_tgt_max_length 30 \
                -model_path "checkpoint/WN18RR-2023-12-01 00:47:11.505860/WN18RR-epoch=047-val_mrr=0.5668.ckpt" \
                -use_prefix_search \
                -gpu 5