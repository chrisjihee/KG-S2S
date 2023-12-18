#export CUDA_VISIBLE_DEVICES=0
#export CUDA_VISIBLE_DEVICES=4
#python3 main.py -dataset FB15k-237N-ko -lr 0.001 -num_beams 40 -seq_dropout 0.2 -use_soft_prompt -use_rel_prompt_emb -src_descrip_max_length 200 -tgt_descrip_max_length 200 -pretrained_model google/mt5-base
python3 main.py -dataset FB15k-237N-ko \
                -lr 0.001 \
                -precision 32 \
                -epoch 15 \
                -batch_size 4 \
                -val_batch_size 2 \
                -num_beams 40 \
                -seq_dropout 0.2 \
                -use_soft_prompt \
                -use_rel_prompt_emb \
                -src_descrip_max_length 200 \
                -tgt_descrip_max_length 200 \
                -eval_tgt_max_length 75 \
                -pretrained_model google/mt5-base
