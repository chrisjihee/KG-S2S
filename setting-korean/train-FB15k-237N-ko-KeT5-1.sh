#export CUDA_VISIBLE_DEVICES=2
#export CUDA_VISIBLE_DEVICES=6
#python3 main.py -dataset FB15k-237N-ko -lr 0.001 -num_beams 40 -seq_dropout 0.2 -use_soft_prompt -use_rel_prompt_emb -src_descrip_max_length 240 -tgt_descrip_max_length 240 -pretrained_model KETI-AIR/ke-t5-base-ko
python3 main.py -dataset FB15k-237N-ko \
                -lr 0.001 \
                -num_beams 40 \
                -seq_dropout 0.2 \
                -use_soft_prompt \
                -use_rel_prompt_emb \
                -src_descrip_max_length 240 \
                -tgt_descrip_max_length 240 \
                -pretrained_model KETI-AIR/ke-t5-base-ko
