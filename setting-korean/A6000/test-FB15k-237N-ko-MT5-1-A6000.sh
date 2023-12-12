#export CUDA_VISIBLE_DEVICES=0
#export CUDA_VISIBLE_DEVICES=4
python3 main.py -dataset FB15k-237N-ko \
                -num_beams 40 \
                -use_soft_prompt \
                -use_rel_prompt_emb \
                -use_prefix_search \
                -src_descrip_max_length 240 \
                -tgt_descrip_max_length 240 \
                -eval_tgt_max_length 90 \
                -model_path "./checkpoint/FB15k-237N-ko-2023-12-12 01:23:46.407204/FB15k-237N-ko-epoch=000-val_mrr=0.1783.ckpt"
