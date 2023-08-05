sort_yaml:
	yq 'sort_keys(..)' src/removesalt/conf/config.yaml | sponge src/removesalt/conf/config.yaml
	yq 'sort_keys(..)' src/removesalt/conf/app/iris.yaml | sponge src/removesalt/conf/app/iris.yaml
	yq 'sort_keys(..)' src/removesalt/conf/app/mediaplayer.yaml | sponge src/removesalt/conf/app/mediaplayer.yaml
	yq 'sort_keys(..)' src/removesalt/conf/app/spectra.yaml | sponge src/removesalt/conf/app/spectra.yaml
