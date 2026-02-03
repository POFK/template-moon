{
  description = "monorepo development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          config.allowUnfree = true;
        };
        shellPkgs = pkgs: with pkgs; [
          proto

          cacert 
          openssl
          zlib

          # 如果你的系统需要编译 Go 代码，可能还需要 gcc/glibc
          gcc 

	  # tools for better command 
          just
          ];

        shellEnv = ''
	  echo "--- 🛡️  Multi-language Dev Environment Loaded ---"
	  echo "Available tools:"
	
	  if command -v proto &> /dev/null; then
	    source <(proto activate)
	    echo "  - proto: $(proto --version)"              
	  fi
	
	  if command -v moon &> /dev/null; then
	    echo "  - moon: $(moon --version)"              
	  fi
	
	  if [[ -n "$BASH_VERSION" && $- == *i* ]]; then
	    if type complete &>/dev/null; then
	      [ -n "$(command -v proto)" ] && source <(proto completions --shell bash)
	      [ -n "$(command -v moon)" ] && source <(moon completions --shell bash)
	      echo "  (Autocomplete scripts loaded)"
	    fi
	  fi
	
	  echo "----------------------------------------------------"
	'';

        # FHS env
        myFhs = pkgs.buildFHSEnv {
          name = "fhs-dev-shell";
          targetPkgs = shellPkgs;
	  profile = ''
          ${shellEnv}

	  export MY_CUSTOM_VAR="fhs-mode"
	  echo "🚀 Entered FHS environment!"
	'';
          runScript = "bash";
        };

      in
      {
        devShells.fhs = myFhs.env;

        devShells.default = pkgs.mkShell {
          buildInputs = shellPkgs pkgs;
          shellHook = ''
          ${shellEnv}

	  export MY_CUSTOM_VAR="default-mode"
	  echo "🚀 Entered non-FHS environment!"
	'';
        };
      }
    );
}
