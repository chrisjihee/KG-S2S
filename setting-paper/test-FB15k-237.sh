python3 main.py -dataset 'FB15k-237' \
                -src_descrip_max_length 80 \
                -tgt_descrip_max_length 80 \
                -use_soft_prompt \
                -use_rel_prompt_emb \
                -num_beams 40 \
                -eval_tgt_max_length 30 \
                -model_path "checkpoint/FB15k-237-2023-12-01 00:45:52.536713/FB15k-237-epoch=032-val_mrr=0.3261.ckpt" \
                -use_prefix_search \
                -gpu 2