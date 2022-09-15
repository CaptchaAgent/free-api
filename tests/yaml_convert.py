# https://raw.githubusercontent.com/QIN2DIM/hcaptcha-challenger/main/src/objects.yaml

import os
import yaml


def main():
    """Run the main function."""
    # Read the YAML file
    with open("objects.yaml", "r", encoding="utf-8") as file:
        data = yaml.load(file, Loader=yaml.FullLoader)

    rdata = {"image_label_binary": []}

    for key, value in data["label_alias"].items():
        print(key, value)
        ritem = {"name": key, "lang": {}}
        for lang, label in value.items():
            label_item = []
            for item in label:
                label_item.append(item)
            ritem["lang"][lang] = label_item
        rdata["image_label_binary"].append(ritem)

    with open(
        os.path.join(
            "..",
            "captchachallenger",
            "challenger",
            "solver",
            "hcaptcha",
            "model_cfg.yaml",
        ),
        "w",
        encoding="utf-8",
    ) as file:
        yaml.dump(
            rdata, file, allow_unicode=True, default_flow_style=None, default_style=None
        )


if __name__ == "__main__":
    main()
