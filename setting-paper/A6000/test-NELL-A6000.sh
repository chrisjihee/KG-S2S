python3 main.py -dataset 'NELL' \
                -src_descrip_max_length 0 \
                -tgt_descrip_max_length 0 \
                -use_soft_prompt \
                -use_rel_prompt_emb \
                -num_beams 40 \
                -eval_tgt_max_length 25 \
                -model_path "checkpoint/NELL-2023-12-08 15:36:47.445695/NELL-epoch=028-val_mrr=0.2264.ckpt" \
                -use_prefix_search \
                -gpu 3