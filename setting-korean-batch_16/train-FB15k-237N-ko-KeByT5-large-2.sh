#export CUDA_VISIBLE_DEVICES=1
#export CUDA_VISIBLE_DEVICES=5
#python3 main.py -dataset FB15k-237N-ko -lr 0.001 -num_beams 40 -seq_dropout 0.2 -use_soft_prompt -use_rel_prompt_emb -src_descrip_max_length 200 -tgt_descrip_max_length 200 -pretrained_model pretrained-pro/ETRI-KEByT5-Base-230426
python3 main.py -dataset FB15k-237N-ko \
                -lr 0.0005 \
                -precision bf16 \
                -epoch 15 \
                -batch_size 16 \
                -val_batch_size 8 \
                -num_beams 40 \
                -seq_dropout 0.2 \
                -use_soft_prompt \
                -use_rel_prompt_emb \
                -src_descrip_max_length 240 \
                -tgt_descrip_max_length 240 \
                -eval_tgt_max_length 90 \
                -pretrained_model pretrained-pro/ETRI-KEByT5-Large-230627
