#python3 main.py -dataset FB15k-237N-ko -lr 0.001 -epoch 1 -batch_size 32 -src_descrip_max_length 80 -tgt_descrip_max_length 80 -use_soft_prompt -use_rel_prompt_emb -seq_dropout 0.2 -num_beams 40 -eval_tgt_max_length 30
python3 main.py -dataset FB15k-237N-ko \
                -lr 0.001 \
                -epoch 50 \
                -batch_size 16 \
                -src_descrip_max_length 240 \
                -tgt_descrip_max_length 240 \
                -use_soft_prompt \
                -use_rel_prompt_emb \
                -seq_dropout 0.2 \
                -num_beams 40 \
                -eval_tgt_max_length 90 \
                -skip_n_val_epoch 0 \
                -pretrained_model etri-lirs/gbst-kebyt5-base-preview \
                -gpu 3