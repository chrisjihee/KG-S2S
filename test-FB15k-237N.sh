python3 main.py -dataset 'FB15k-237N' \
                -src_descrip_max_length 80 \
                -tgt_descrip_max_length 80 \
                -use_soft_prompt \
                -use_rel_prompt_emb \
                -num_beams 40 \
                -eval_tgt_max_length 30 \
                -model_path "checkpoint/FB15k-237N-2023-12-01 00:47:25.667747/FB15k-237N-epoch=032-val_mrr=0.3419.ckpt" \
                -use_prefix_search \
                -gpu 6