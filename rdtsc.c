#include<stdio.h>
#include <windows.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>
#include<conio.h>
int rdtsc_check();
int vmexit_check();
static inline unsigned long long rdtscd() {
	unsigned long long ret, ret2;
	unsigned eax, edx;
	__asm__ volatile("rdtsc" : "=a" (eax), "=d" (edx));
	ret  = ((unsigned long long)eax) | (((unsigned long long)edx) << 32);
	__asm__ volatile("rdtsc" : "=a" (eax), "=d" (edx));
	ret2  = ((unsigned long long)eax) | (((unsigned long long)edx) << 32);
	return ret2 - ret;
}
static inline unsigned long long rdtscd_vmexit() {
	unsigned long long ret, ret2;
	unsigned eax, edx;
	__asm__ volatile("rdtsc" : "=a" (eax), "=d" (edx));
	ret  = ((unsigned long long)eax) | (((unsigned long long)edx) << 32);

	__asm__ volatile("cpuid" : /* no output */ : "a"(0x00));

	__asm__ volatile("rdtsc" : "=a" (eax), "=d" (edx));
	ret2  = ((unsigned long long)eax) | (((unsigned long long)edx) << 32);
	return ret2 - ret;
}
int rdtsc_check() {
	int i;
	unsigned long long average = 0;
	for (i = 0; i < 10; i++) {
		average = average + rdtscd();
		Sleep(500);
	}
	average = average / 10;
	return (average < 750 && average > 0) ? FALSE : TRUE;
}
int vmexit_check() {
	int i;
	unsigned long long average = 0;
	for (i = 0; i < 10; i++) {
		average = average + rdtscd_vmexit();
		Sleep(500);
	}
	average = average / 10;
	return (average < 1000 && average > 0) ? FALSE : TRUE;
}
void run(char * text, int (*callback)(), char * log, char * text_trace) {
	int output;
	int (*callback_writeslog)(int) = callback;
	if (log)
		output = callback();
	else
		output = callback_writeslog(TRUE);
	printf("\n%s:", text);
	if (output == TRUE) {
		if (log)
		printf(" Detected");
	}
	else printf(" Passed");
}
int main(void){
	    run("RDTSC Check(0)",&rdtsc_check,"trace rdtsc differences", "rdtsc_test");
		run("RDTSC Exit VM Check (0)",&vmexit_check,"trace forcing VM exit","vm_exit_test");
}







