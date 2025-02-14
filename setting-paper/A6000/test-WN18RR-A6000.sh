python3 main.py -dataset 'WN18RR' \
                -src_descrip_max_length 40 \
                -tgt_descrip_max_length 10 \
                -use_soft_prompt \
                -use_rel_prompt_emb \
                -num_beams 40 \
                -eval_tgt_max_length 30 \
                -model_path "checkpoint/WN18RR-2023-12-01 01:00:23.464637/WN18RR-epoch=092-val_mrr=0.5759.ckpt" \
                -use_prefix_search \
                -gpu 0