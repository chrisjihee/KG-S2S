python3 main.py -dataset FB15k-237N-ko \
                -num_beams 40 \
                -use_soft_prompt \
                -use_rel_prompt_emb \
                -use_prefix_search \
                -src_descrip_max_length 240 \
                -tgt_descrip_max_length 240 \
                -eval_tgt_max_length 90 \
                -model_path "checkpoint/FB15k-237N-ko-2023-12-11 14:18:56.295543/FB15k-237N-ko-epoch=000-val_mrr=0.8752.ckpt" \
                -gpu 7
