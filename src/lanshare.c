#include <stdio.h>
#include <stdlib.h>

#define OK 0
#define ERR 1

int
search_hosts()
{
	return OK;
}

int
main(int argc, char *argv[])
{
	int ret = 0;

	printf("Searching...\n");

	ret = search_hosts();

	if (ret != OK)
		fprintf(stderr, "Couldn't find any hosts\n");

	return 0;
}
