#python3 main.py -dataset FB15k-237N-ko -lr 0.001 -num_beams 40 -seq_dropout 0.2 -use_soft_prompt -use_rel_prompt_emb -pretrained_model google/mt5-base -src_descrip_max_length 240 -tgt_descrip_max_length 240 -eval_tgt_max_length 90 -batch_size 16 -skip_n_val_epoch 0 -epoch 1 -gpu 0
export CUDA_VISIBLE_DEVICES=0,1
python3 main.py -dataset FB15k-237N-ko \
                -lr 0.001 \
                -num_beams 40 \
                -seq_dropout 0.2 \
                -use_soft_prompt \
                -use_rel_prompt_emb \
                -pretrained_model google/mt5-base \
                -src_descrip_max_length 240 \
                -tgt_descrip_max_length 240 \
                -eval_tgt_max_length 90 \
                -accelerator gpu \
                -batch_size 16 \
                -precision 16 \
                -devices 2 \
                -epoch 3
