python3 main.py -dataset 'ICEWS14' \
                -src_descrip_max_length 40 \
                -tgt_descrip_max_length 40 \
                -temporal  \
                -use_soft_prompt \
                -use_rel_prompt_emb \
                -num_beams 40 \
                -eval_tgt_max_length 26 \
                -model_path path/to/trained/model \
                -use_prefix_search