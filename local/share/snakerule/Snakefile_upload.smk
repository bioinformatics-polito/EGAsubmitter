include: "../snakemake/conf_upload.sk"

rule fastq_upload:
    input: lambda wildcards: METADATA[wildcards.batch]
    output: touch("fastq_upload-{batch}.done")
    params: tool=PDX2GODOT, batch="{batch}", outpath=OUTPUT_DIR
    shell:
        """
            {params.tool} {params.batch} {input} {params.outpath}
        """