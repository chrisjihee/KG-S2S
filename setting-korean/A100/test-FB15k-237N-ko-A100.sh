python3 main.py -dataset FB15k-237N-ko \
                -src_descrip_max_length 80 \
                -tgt_descrip_max_length 80 \
                -use_soft_prompt \
                -use_rel_prompt_emb \
                -num_beams 40 \
                -eval_tgt_max_length 30 \
                -model_path "checkpoint/FB15k-237N-ko-2023-12-08 23:24:46.524169/FB15k-237N-ko-epoch=004-val_mrr=0.8944.ckpt" \
                -use_prefix_search \
                -gpu 7