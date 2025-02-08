# NOTE(krishan711): --legacy-peer-deps because of conflict between ui-react pre-realease and ui-react-toast requirements
install:
	@ npm ci --legacy-peer-deps

install-updates:
	@ npm install

list-outdated: install
	@ npm outdated

lint-check:
	@ npx lint

lint-check-ci:
	@ npx lint --output-file lint-check-results.json --output-file-format annotations

lint-fix:
	@ npx lint --fix

type-check:
	@ npx type-check

type-check-ci:
	@ npx type-check --output-file type-check-results.json --output-file-format annotations

security-check:
	@ # NOTE(krishan711): maybe use npm audit
	@ echo "Not Supported"

security-check-ci:
	@ echo "Not Supported"

build:
	@ npx build-react-app --config-modifier ./config.build.js

build-ssr:
	@ npx build-react-app-ssr --config-modifier ./config.build.js

build-static:
	@ npx build-react-app-static --config-modifier ./config.build.js

start:
	@ npx build-react-app --start --dev --config-modifier ./config.build.js

start-prod:
	@ npx build-react-app --start --config-modifier ./config.build.js

test:
	@ echo "Not Supported"

clean:
	@ rm -rf ./node_modules ./package-lock.json ./build ./dist

.PHONY: *
