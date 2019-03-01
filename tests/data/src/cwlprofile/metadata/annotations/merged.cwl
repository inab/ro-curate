{
    "$graph": [
        {
            "class": "Workflow",
            "label": "Unaligned to aligned BAM",
            "requirements": [
                {
                    "class": "ScatterFeatureRequirement"
                },
                {
                    "class": "SubworkflowFeatureRequirement"
                },
                {
                    "class": "MultipleInputFeatureRequirement"
                }
            ],
            "inputs": [
                {
                    "type": "File",
                    "id": "#main/bam"
                },
                {
                    "type": "string",
                    "id": "#main/readgroup"
                },
                {
                    "type": "string",
                    "id": "#main/reference"
                }
            ],
            "outputs": [
                {
                    "type": "File",
                    "outputSource": "#main/align_and_tag/aligned_bam",
                    "id": "#main/tagged_bam"
                }
            ],
            "steps": [
                {
                    "run": "#align_and_tag.cwl",
                    "in": [
                        {
                            "source": "#main/bam",
                            "id": "#main/align_and_tag/bam"
                        },
                        {
                            "source": "#main/readgroup",
                            "id": "#main/align_and_tag/readgroup"
                        },
                        {
                            "source": "#main/reference",
                            "id": "#main/align_and_tag/reference"
                        }
                    ],
                    "out": [
                        "#main/align_and_tag/aligned_bam"
                    ],
                    "id": "#main/align_and_tag"
                }
            ],
            "id": "#main"
        },
        {
            "class": "CommandLineTool",
            "label": "align with bwa_mem and tag",
            "baseCommand": [
                "/bin/bash",
                "/usr/bin/alignment_helper.sh"
            ],
            "requirements": [
                {
                    "class": "ResourceRequirement",
                    "coresMin": 8,
                    "ramMin": 20000
                }
            ],
            "stdout": "refAlign.bam",
            "arguments": [
                {
                    "position": 4,
                    "valueFrom": "$(runtime.cores)"
                }
            ],
            "inputs": [
                {
                    "type": "File",
                    "inputBinding": {
                        "position": 1
                    },
                    "id": "#align_and_tag.cwl/bam"
                },
                {
                    "type": "string",
                    "inputBinding": {
                        "position": 2
                    },
                    "id": "#align_and_tag.cwl/readgroup"
                },
                {
                    "type": "string",
                    "inputBinding": {
                        "position": 3
                    },
                    "id": "#align_and_tag.cwl/reference"
                }
            ],
            "outputs": [
                {
                    "type": "stdout",
                    "id": "#align_and_tag.cwl/aligned_bam"
                }
            ],
            "id": "#align_and_tag.cwl"
        }
    ],
    "cwlVersion": "v1.0"
}
