# aolney_jupyterlab_metadata_html_extension

[![Github Actions Status](https://github.com/aolney/jupyterlab-metadata-html-extension/workflows/Build/badge.svg)](https://github.com/aolney/jupyterlab-metadata-html-extension/actions/workflows/build.yml)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/aolney/jupyterlab-metadata-html-extension/main?urlpath=lab)


A JupyterLab extension that uses cell metadata to define html that is injected into markdown cells.

This approach overcomes the limitations of JupyterLab markdown cells for certain types of html, such as iframes, that appear to be stripped/sanitized based on the JupyterLab security model.

Using this extension therefore increases the likelihood that an attacker may use a notebook to execute arbitrary code on your computer.

This extension is meant for research purposes only and is not meant for general usage. 

Obviously, notebooks with html in the metadata will not render properly without this extension. 

Example metadata:

```javascript
{
    "html": "<iframe class='metadata-html' width='560' height='315' src='https://www.youtube.com/embed/nBrKsT1IvIM' frameborder='0' allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture' allowfullscreen></iframe>"
}
```

`class='metadata-html'` will prevent duplicate html injection if switching between notebooks.

> [!NOTE]
> This repo renames and replaces the [Jupyter 1.2x version written in F#](https://github.com/aolney/metadata-html-extension).

## Requirements

- JupyterLab >= 4.0.0

## Install

To install the extension, execute:

```bash
pip install aolney_jupyterlab_metadata_html_extension
```

## Uninstall

To remove the extension, execute:

```bash
pip uninstall aolney_jupyterlab_metadata_html_extension
```

## Contributing

### Development install

Note: You will need NodeJS to build the extension package.

The `jlpm` command is JupyterLab's pinned version of
[yarn](https://yarnpkg.com/) that is installed with JupyterLab. You may use
`yarn` or `npm` in lieu of `jlpm` below.

```bash
# Clone the repo to your local environment
# Change directory to the aolney_jupyterlab_metadata_html_extension directory
# Install package in development mode
pip install -e "."
# Link your development version of the extension with JupyterLab
jupyter labextension develop . --overwrite
# Rebuild extension Typescript source after making changes
jlpm build
```

You can watch the source directory and run JupyterLab at the same time in different terminals to watch for changes in the extension's source and automatically rebuild the extension.

```bash
# Watch the source directory in one terminal, automatically rebuilding when needed
jlpm watch
# Run JupyterLab in another terminal
jupyter lab
```

With the watch command running, every saved change will immediately be built locally and available in your running JupyterLab. Refresh JupyterLab to load the change in your browser (you may need to wait several seconds for the extension to be rebuilt).

By default, the `jlpm build` command generates the source maps for this extension to make it easier to debug using the browser dev tools. To also generate source maps for the JupyterLab core extensions, you can run the following command:

```bash
jupyter lab build --minimize=False
```

### Development uninstall

```bash
pip uninstall aolney_jupyterlab_metadata_html_extension
```

In development mode, you will also need to remove the symlink created by `jupyter labextension develop`
command. To find its location, you can run `jupyter labextension list` to figure out where the `labextensions`
folder is located. Then you can remove the symlink named `@aolney/jupyterlab-metadata-html-extension` within that folder.

### Packaging the extension

See [RELEASE](RELEASE.md)
