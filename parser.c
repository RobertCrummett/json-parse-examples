//
// https://github.com/lotabout/write-a-C-interpreter/blob/master/tutorial/en/3-Lexer.md
//
#include <errno.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void read_entire_file_to_cstr(const char *path, char **data) {
	//
	// Open the file for reading
	//
	FILE *file = fopen(path, "r");
	if (ferror(file)) {
		fprintf(stderr, "ERROR while opening %s: %s\n", path, strerror(errno));
		return;
	}
	//
	// Find the end of the file
	// Non-zero exit code is an error
	//
	if (fseek(file, 0, SEEK_END)) {
		fprintf(stderr, "ERROR while seeking end of %s: %s\n", path, strerror(errno));
		fclose(file);
		return;
	}
	//
	// Report the length of the file in bytes
	// If -1, this means that there was an error
	//
	long length = ftell(file);
	if (length == -1) {
		fprintf(stderr, "ERROR determining size (in bytes) of %s: %s\n", path, strerror(errno));
		fclose(file);
		return;
	}
	//
	// Rewind the file to the beginning
	// Non-zero exit code is an error
	//
	if (fseek(file, 0, SEEK_SET)) {
		fprintf(stderr, "ERROR while rewinding %s: %s\n", path, strerror(errno));
		fclose(file);
		return;
	}
	//
	// Allocate space for the file in memory
	//
	*data = malloc(length);
	if (*data == NULL) { 
		fprintf(stderr, "ERROR allocating memory (%ld bytes) for %s: %s\n", length, path, strerror(errno));
		fclose(file);
		return;
	}
	//
	// Read the file contents into memory
	// Exit code not equal to 1 means that 1 output was not read into memory.
	//
	if (fread(*data, length, 1, file) != 1) {
		fprintf(stderr, "ERROR reading %s into memory: %s\n", path, strerror(errno));
		fclose(file);
		free(data);
		return;
	};
	fclose(file);
}

enum {
	json_Object = 128, json_Array, json_String, json_Number, json_True, json_False, json_Null
};

void next() {
	char *last_pos;
	uint32_t hash;
	while (token = *src) {
		++src;
		// parse token here
		// ...
		if (token == '\n') {
			++line;
		}
		// ...
	}
	return;
}

int main(void) {
	//
	// Read file into string
	//
	const char *path = "share/example.json";
	char *data = NULL;
	read_entire_file_to_cstr(path, &data);

	return 0;
}
