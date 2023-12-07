#python3 main.py -dataset 'NELL' -lr 0.0005 -epoch 30 -batch_size 128 -src_descrip_max_length 0 -tgt_descrip_max_length 0 -use_soft_prompt -use_rel_prompt_emb -num_beams 40 -eval_tgt_max_length 25 -skip_n_val_epoch 15 -gpu 3
python3 main.py -dataset 'NELL' \
                -lr 0.0005 \
                -epoch 30 \
                -batch_size 128 \
                -src_descrip_max_length 0 \
                -tgt_descrip_max_length 0 \
                -use_soft_prompt \
                -use_rel_prompt_emb \
                -num_beams 40 \
                -eval_tgt_max_length 25 \
                -skip_n_val_epoch 15 \
                -gpu 3