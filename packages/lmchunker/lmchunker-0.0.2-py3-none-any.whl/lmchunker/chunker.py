from typing import List


def chunker(text,small_model,small_tokenizer,language,methodth='ppl',threshold=0,dynamic_merge='no',target_size=200,batch_size=4096,max_txt_size=9000) -> List[str]:
    # text: Text that needs to be segmented
    # language: en or zh
    # method: LLM chunking method that needs to be used, ['ppl','ms']
    # threshold: The threshold for controlling PPL Chunking is inversely proportional to the chunk length; the smaller the threshold, the shorter the chunk length.
    # dynamic_merge: no or yes
    # target_size: If dynamic_merge='yes', then the chunk length value needs to be set

    # When dealing with longer documents (exceeding 4096 characters), it is recommended to use KV caching to optimize GPU memory usage. 
    # The batch_size refers to the length of a single document processed at a time. 
    # The max_txt_size represents the total context length that can be considered or the maximum length that the GPU memory can accommodate.

    if methodth=='ppl':
        from modules.ppl_chunking import llm_chunker_ppl
        chunks=llm_chunker_ppl(text,small_model,small_tokenizer,threshold,language,dynamic_merge=dynamic_merge,target_size=target_size,batch_size=batch_size,max_txt_size=max_txt_size)  
    elif methodth=='ms':
        from modules.margin_sampling_chunking import llm_chunker_ms
        chunks=llm_chunker_ms(text,small_model,small_tokenizer,language,dynamic_merge,target_size)  
        
    return chunks
