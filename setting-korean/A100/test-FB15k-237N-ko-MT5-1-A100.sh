#export CUDA_VISIBLE_DEVICES=0
#export CUDA_VISIBLE_DEVICES=4
python3 main.py -dataset FB15k-237N-ko \
                -num_beams 40 \
                -use_soft_prompt \
                -use_rel_prompt_emb \
                -use_prefix_search \
                -pretrained_model google/mt5-base \
                -src_descrip_max_length 240 \
                -tgt_descrip_max_length 240 \
                -eval_tgt_max_length 90 \
                -precision bf16 \
                -val_batch_size 16 \
                -batch_size 16 \
                -model_path "./checkpoint/FB15k-237N-ko-2023-12-12 01:28:28.476108/FB15k-237N-ko-epoch=000-val_mrr=0.1385.ckpt"
