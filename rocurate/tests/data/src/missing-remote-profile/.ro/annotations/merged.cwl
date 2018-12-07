{
    "$graph": [
        {
            "class": "CommandLineTool",
            "id": "#adtex.cwl",
            "label": "ADTEx workflow",
            "requirements": [
                {
                    "class": "DockerRequirement",
                    "dockerPull": "quay.io/ucsc_cgl/dockstore_tool_adtex:v1.0.0"
                }
            ],
            "baseCommand": [
                "-o",
                "./",
                "--tostdout"
            ],
            "doc": "Docker container for an ADTEx workflow. See the [github repo](https://github.com/BD2KGenomics/dockstore_tool_adtex.git) for more information.",
            "inputs": [
                {
                    "type": "File",
                    "doc": "Centromere bed file",
                    "format": "http://edamontology.org/format_3003",
                    "inputBinding": {
                        "prefix": "-c"
                    },
                    "id": "#adtex.cwl/centromeres"
                },
                {
                    "type": "File",
                    "doc": "The control exome BAM file used as input, it must be sorted.",
                    "format": "http://edamontology.org/format_2572",
                    "inputBinding": {
                        "prefix": "-n"
                    },
                    "id": "#adtex.cwl/control_bam_input"
                },
                {
                    "type": [
                        "null",
                        "string"
                    ],
                    "default": "myPatient",
                    "doc": "sample ID to use in output",
                    "inputBinding": {
                        "prefix": "-s"
                    },
                    "id": "#adtex.cwl/sample_id"
                },
                {
                    "type": "File",
                    "doc": "Exome Targets bed file",
                    "format": "http://edamontology.org/format_3003",
                    "inputBinding": {
                        "prefix": "-b"
                    },
                    "id": "#adtex.cwl/targets"
                },
                {
                    "type": "File",
                    "doc": "The tumor exome BAM file used as input, it must be sorted.",
                    "format": "http://edamontology.org/format_2572",
                    "inputBinding": {
                        "prefix": "-t"
                    },
                    "id": "#adtex.cwl/tumor_bam_input"
                }
            ],
            "stdout": "adtex.cnv",
            "outputs": [
                {
                    "type": "stdout",
                    "id": "#adtex.cwl/output"
                }
            ]
        },
        {
            "class": "Workflow",
            "doc": "Copynumber variation workflow, runs ADTEx and Varscan",
            "requirements": [
                {
                    "class": "MultipleInputFeatureRequirement"
                },
                {
                    "class": "StepInputExpressionRequirement"
                },
                {
                    "class": "InlineJavascriptRequirement"
                }
            ],
            "inputs": [
                {
                    "type": "File",
                    "id": "#main/CENTROMERES"
                },
                {
                    "type": "File",
                    "id": "#main/GENO_FA_GZ"
                },
                {
                    "type": "File",
                    "id": "#main/NORMAL_BAM"
                },
                {
                    "type": "string",
                    "id": "#main/SAMPLE_ID"
                },
                {
                    "type": "File",
                    "id": "#main/TARGETS"
                },
                {
                    "type": "File",
                    "id": "#main/TUMOR_BAM"
                }
            ],
            "outputs": [
                {
                    "type": "File",
                    "outputSource": "#main/adtex/output",
                    "id": "#main/ADTEX_OUTCNV"
                },
                {
                    "type": "File",
                    "outputSource": "#main/varscan/output",
                    "id": "#main/VARSCAN_OUTCNV"
                }
            ],
            "steps": [
                {
                    "run": "#adtex.cwl",
                    "in": [
                        {
                            "source": "#main/CENTROMERES",
                            "id": "#main/adtex/centromeres"
                        },
                        {
                            "source": "#main/NORMAL_BAM",
                            "id": "#main/adtex/control_bam_input"
                        },
                        {
                            "source": "#main/SAMPLE_ID",
                            "id": "#main/adtex/sample_id"
                        },
                        {
                            "source": "#main/TARGETS",
                            "id": "#main/adtex/targets"
                        },
                        {
                            "source": "#main/TUMOR_BAM",
                            "id": "#main/adtex/tumor_bam_input"
                        }
                    ],
                    "out": [
                        "#main/adtex/output"
                    ],
                    "id": "#main/adtex"
                },
                {
                    "run": "#varscan_cnv.cwl",
                    "in": [
                        {
                            "source": "#main/CENTROMERES",
                            "id": "#main/varscan/centromeres"
                        },
                        {
                            "source": "#main/NORMAL_BAM",
                            "id": "#main/varscan/control_bam_input"
                        },
                        {
                            "source": "#main/zcat/unzippedFile",
                            "id": "#main/varscan/genome"
                        },
                        {
                            "source": "#main/SAMPLE_ID",
                            "id": "#main/varscan/sample_id"
                        },
                        {
                            "source": "#main/TARGETS",
                            "id": "#main/varscan/targets"
                        },
                        {
                            "source": "#main/TUMOR_BAM",
                            "id": "#main/varscan/tumor_bam_input"
                        }
                    ],
                    "out": [
                        "#main/varscan/output"
                    ],
                    "id": "#main/varscan"
                },
                {
                    "run": "#zcat.cwl",
                    "in": [
                        {
                            "source": "#main/GENO_FA_GZ",
                            "id": "#main/zcat/gzipFile"
                        },
                        {
                            "valueFrom": "$('genome.fa')",
                            "id": "#main/zcat/unzippedFileName"
                        }
                    ],
                    "out": [
                        "#main/zcat/unzippedFile"
                    ],
                    "id": "#main/zcat"
                }
            ],
            "id": "#main"
        },
        {
            "class": "CommandLineTool",
            "id": "#varscan_cnv.cwl",
            "label": "Varscan2 workflow",
            "baseCommand": [
                "-s",
                "./"
            ],
            "doc": "A Docker container for a Varscan2 workflow. See the [github repo](https://github.com/BD2KGenomics/dockstore_tool_varscan_cnv.git) for more information.",
            "requirements": [
                {
                    "class": "DockerRequirement",
                    "dockerPull": "quay.io/ucsc_cgl/dockstore_tool_varscan_cnv:v1.0.0"
                }
            ],
            "inputs": [
                {
                    "type": "File",
                    "doc": "Centromere bed file",
                    "format": "http://edamontology.org/format_3003",
                    "inputBinding": {
                        "prefix": "-b"
                    },
                    "id": "#varscan_cnv.cwl/centromeres"
                },
                {
                    "type": "File",
                    "doc": "The control exome BAM file used as input, it must be sorted.",
                    "format": "http://edamontology.org/format_2572",
                    "inputBinding": {
                        "prefix": "-c"
                    },
                    "id": "#varscan_cnv.cwl/control_bam_input"
                },
                {
                    "type": "File",
                    "doc": "Genome fasta",
                    "format": "http://edamontology.org/format_1929",
                    "inputBinding": {
                        "prefix": "-i"
                    },
                    "id": "#varscan_cnv.cwl/genome"
                },
                {
                    "type": [
                        "null",
                        "string"
                    ],
                    "default": "mypatient",
                    "doc": "sample ID to use in output",
                    "inputBinding": {
                        "prefix": "-q"
                    },
                    "id": "#varscan_cnv.cwl/sample_id"
                },
                {
                    "type": "File",
                    "doc": "Exome Targets bed file",
                    "format": "http://edamontology.org/format_3003",
                    "inputBinding": {
                        "prefix": "-w"
                    },
                    "id": "#varscan_cnv.cwl/targets"
                },
                {
                    "type": "File",
                    "doc": "The tumor exome BAM file used as input, it must be sorted.",
                    "format": "http://edamontology.org/format_2572",
                    "inputBinding": {
                        "prefix": "-t"
                    },
                    "id": "#varscan_cnv.cwl/tumor_bam_input"
                }
            ],
            "stdout": "varscan.cnv",
            "outputs": [
                {
                    "id": "#varscan_cnv.cwl/output",
                    "type": "stdout"
                }
            ]
        },
        {
            "class": "CommandLineTool",
            "baseCommand": "zcat",
            "stdout": "$(inputs.unzippedFileName)",
            "inputs": [
                {
                    "type": "File",
                    "inputBinding": {
                        "position": 1
                    },
                    "id": "#zcat.cwl/gzipFile"
                },
                {
                    "type": "string",
                    "id": "#zcat.cwl/unzippedFileName"
                }
            ],
            "outputs": [
                {
                    "type": "stdout",
                    "id": "#zcat.cwl/unzippedFile"
                }
            ],
            "id": "#zcat.cwl"
        }
    ],
    "cwlVersion": "v1.0"
}
