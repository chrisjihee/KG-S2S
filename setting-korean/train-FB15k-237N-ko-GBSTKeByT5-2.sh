#export CUDA_VISIBLE_DEVICES=2
#export CUDA_VISIBLE_DEVICES=6
#python3 main.py -dataset FB15k-237N-ko -lr 0.0005 -num_beams 40 -seq_dropout 0.2 -use_soft_prompt -use_rel_prompt_emb -pretrained_model pretrained-pro/ETRI-KEByT5-Base-GBST_ds3x-230627 -src_descrip_max_length 240 -tgt_descrip_max_length 240 -eval_tgt_max_length 90 -precision bf16 -val_batch_size 16 -batch_size 16 -epoch 3
python3 main.py -dataset FB15k-237N-ko \
                -lr 0.0005 \
                -num_beams 40 \
                -seq_dropout 0.2 \
                -use_soft_prompt \
                -use_rel_prompt_emb \
                -pretrained_model pretrained-pro/ETRI-KEByT5-Base-GBST_ds3x-230627 \
                -src_descrip_max_length 240 \
                -tgt_descrip_max_length 240 \
                -eval_tgt_max_length 90 \
                -precision bf16 \
                -val_batch_size 16 \
                -batch_size 16 \
                -epoch 3
