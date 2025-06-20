#!/bin/bash


FIRST="$1"

7z x "$1" -o./extracted_files/


try_passwords_to_extract() {
    local archive="$1"
    shift
    local passwords=("$@")

    if [[ ! -f "$archive" ]]; then
        echo "❌ File not found: $archive"
        return 1
    fi

    local extension="${archive##*.}"

    for password in "${passwords[@]}"; do
        echo "🔑 Trying password: $password"

        if [[ "$extension" == "zip" ]]; then
            unzip -P "$password" -t "$archive" >/dev/null 2>&1
            if [[ $? -eq 0 ]]; then
                echo "✅ Correct password: $password"
                unzip -P "$password" "$archive"
                return 0
            fi
        elif [[ "$extension" == "7z" ]]; then
            7z t -p"$password" "$archive" >/dev/null 2>&1
            if [[ $? -eq 0 ]]; then
                echo "✅ Correct password: $password"
                7z x -p"$password" "$archive"
                return 0
            fi
        else
            echo "❌ Unsupported file type: $extension"
            return 2
        fi
    done

    echo "❌ No valid password found."
    return 1
}



while true; do

  for file in ./extracted_files/*; do
    if [[ -f "$file" && "$file" != *.zip && "$file" != *.7z ]]; then
      passw=$(cat "$file")
      cat "$file" >> password.txt
      base32=$(echo -n "$passw" | base32)
      base64=$(echo -n "$passw" | base64)
      hex=$(echo -n "$passw" | xxd -p)
        # Do something with "$file"
    fi
  done

  echo "\n" >> password.txt

  zip_file=$(compgen -G "./extracted_files/*.zip" | head -n 1)
  sevenz_file=$(compgen -G "./extracted_files/*.7z" | head -n 1)

  if [[ -n "$zip_file" ]]; then
    try_passwords_to_extract "$zip_file" "$passw" "$base32" "$base64" "$hex"
    # unzip "$zip_file"
  elif [[ -n "$sevenz_file" ]]; then
    try_passwords_to_extract "$sevenz_file" "$passw" "$base32" "$base64" "$hex"
    # 7z x "$sevenz_file"
  else
     echo "No .zip or .7z files found"
  fi

  rm -rf ./extracted_files
  mkdir extracted_files
  
  for file in *; do
    if [[ -f "$file" && "$file" != *.sh && "$file" != *.txt ]]; then
        mv "$file" extracted_files/
    fi
  done

done
