# rule pre_join:
#     input: expand("results/{genome}_done.txt", zip, genome=config["genomes"])
#     output: "results/all_genomes_done.txt"
#     log: "logs/all/prejoin.log"
#     shell: "echo done > {output}"

# rule get_data:
#     input: "{genome}"
#     output: "data/{genome}"
#     log: "logs/general/{genome}_get_data.log"
#     shell: "cp {input} data 2> {log}"
