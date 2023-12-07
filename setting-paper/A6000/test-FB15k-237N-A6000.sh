python3 main.py -dataset 'FB15k-237N' \
                -src_descrip_max_length 80 \
                -tgt_descrip_max_length 80 \
                -use_soft_prompt \
                -use_rel_prompt_emb \
                -num_beams 40 \
                -eval_tgt_max_length 30 \
                -model_path "checkpoint/FB15k-237N-2023-12-01 01:00:40.119624/FB15k-237N-epoch=041-val_mrr=0.3476.ckpt" \
                -use_prefix_search \
                -gpu 1