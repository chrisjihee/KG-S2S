python3 main.py -dataset 'WN18RR' \
                -src_descrip_max_length 40 \
                -tgt_descrip_max_length 10 \
                -use_soft_prompt \
                -use_rel_prompt_emb \
                -num_beams 40 \
                -eval_tgt_max_length 30 \
                -model_path "checkpoint/WN18RR-2023-12-01 00:07:10.531228/WN18RR-epoch=074-val_mrr=0.5730.ckpt" \
                -use_prefix_search \
                -gpu 1