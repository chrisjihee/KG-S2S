#export CUDA_VISIBLE_DEVICES=2
#export CUDA_VISIBLE_DEVICES=6
python3 main.py -dataset FB15k-237N-ko \
                -num_beams 40 \
                -use_soft_prompt \
                -use_rel_prompt_emb \
                -use_prefix_search \
                -pretrained_model KETI-AIR/ke-t5-base-ko \
                -src_descrip_max_length 240 \
                -tgt_descrip_max_length 240 \
                -eval_tgt_max_length 90 \
                -precision bf16 \
                -val_batch_size 16 \
                -batch_size 16 \
                -model_path "./checkpoint/FB15k-237N-ko-2023-12-12 01:28:49.913116/FB15k-237N-ko-epoch=002-val_mrr=0.2285.ckpt"
