#python3 main.py -dataset FB15k-237-ko -lr 0.001 -epoch 1 -batch_size 32 -src_descrip_max_length 80 -tgt_descrip_max_length 80 -use_soft_prompt -use_rel_prompt_emb -seq_dropout 0.2 -num_beams 40 -eval_tgt_max_length 30
python3 main.py -dataset FB15k-237-ko \
                -lr 0.001 \
                -epoch 40 \
                -batch_size 32 \
                -src_descrip_max_length 80 \
                -tgt_descrip_max_length 80 \
                -use_soft_prompt \
                -use_rel_prompt_emb \
                -seq_dropout 0.2 \
                -num_beams 40 \
                -eval_tgt_max_length 30 \
                -skip_n_val_epoch 1 \
                -pretrained_model mt5-base \
                -gpu 0