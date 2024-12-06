from chemloader import MolDataLoader, DataDownloader, SmilesCsvToStorage


class MorganFlashPoint(MolDataLoader):
    expected_data_size = 14696
    expected_mol = 8584
    citation = "https://doi.org/10.1002/minf.201900101"

    setup_pipleline = [
        DataDownloader(
            src="https://figshare.com/ndownloader/files/18509711",
            raw_file_name="morgan_fp.csv",
        ),
        SmilesCsvToStorage(
            smiles="smiles",
            bool_props={
                "pure substance": "pure_substance",
                "is_silicon": "is_silicon",
                "is_metallic": "is_metallic",
                "is_tin": "is_tin",
                "is_acid": "is_acid",
            },
        ),
    ]
