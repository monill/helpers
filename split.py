import os

# Define the input file name and the output file prefix
input_file = "blocked.txt"
output_prefix = "blocked_"

# Define the chunk size in bytes
chunk_size = 1024 * 1024 * 90  # 90 MB

# Open the input file for reading in binary mode
with open(input_file, "rb") as f:
    chunk_number = 0
    while True:
        # Read the next chunk from the input file
        chunk = f.read(chunk_size)
        if not chunk:
            # End of file
            break

        # Write the chunk to a new output file
        chunk_number += 1
        output_file_name = f"{output_prefix}{chunk_number}.txt"
        with open(output_file_name, "wb") as output_file:
            output_file.write(chunk)

# Print a message indicating how many chunks were created
num_chunks = chunk_number
print(f"{num_chunks} output files created.")
