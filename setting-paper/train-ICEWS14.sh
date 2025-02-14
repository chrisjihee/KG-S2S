#python3 main.py -dataset ICEWS14 -lr 0.0005 -epoch 1 -batch_size 32 -src_descrip_max_length 40 -tgt_descrip_max_length 40 -temporal -use_soft_prompt -use_rel_prompt_emb -seq_dropout 0.1 -num_beams 40 -eval_tgt_max_length 26
python3 main.py -dataset ICEWS14 \
                -lr 0.0005 \
                -epoch 100 \
                -batch_size 32 \
                -src_descrip_max_length 40 \
                -tgt_descrip_max_length 40 \
                -temporal \
                -use_soft_prompt \
                -use_rel_prompt_emb \
                -seq_dropout 0.1 \
                -num_beams 40 \
                -eval_tgt_max_length 26 \
                -skip_n_val_epoch 50 \
                -gpu 2