python3 main.py -dataset 'ICEWS14' \
                -src_descrip_max_length 40 \
                -tgt_descrip_max_length 40 \
                -temporal  \
                -use_soft_prompt \
                -use_rel_prompt_emb \
                -num_beams 40 \
                -eval_tgt_max_length 26 \
                -model_path "checkpoint/ICEWS14-2023-12-01 00:58:52.211480/ICEWS14-epoch=053-val_mrr=0.6039.ckpt" \
                -use_prefix_search \
                -gpu 2