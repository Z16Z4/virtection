#include<stdio.h>
#include <windows.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>
#include<conio.h>
/*variable for rdtsc check*/
int rdtsc_check();
/*variable for vmexit*/
int vmexit_check();
/* inline usigned long long rdtscd >> ret1 & 2*/
static inline unsigned long long rdtscd() {
	unsigned long long ret, ret2;
	unsigned eax, edx;
	__asm__ volatile("rdtsc" : "=a" (eax), "=d" (edx));
    /*pipe ret binary left shift 32*/
	ret  = ((unsigned long long)eax) | (((unsigned long long)edx) << 32);
	__asm__ volatile("rdtsc" : "=a" (eax), "=d" (edx));
    /*pipe into ret 2 binary left shift 32*/
	ret2  = ((unsigned long long)eax) | (((unsigned long long)edx) << 32);
	return ret2 - ret;
}
static inline unsigned long long rdtscd_vmexit() {
	unsigned long long ret, ret2;
	unsigned eax, edx;
	__asm__ volatile("rdtsc" : "=a" (eax), "=d" (edx));
	ret  = ((unsigned long long)eax) | (((unsigned long long)edx) << 32);
    /*cpuid 0x00 no output*/
	__asm__ volatile("cpuid" : /* no output */ : "a"(0x00));
	__asm__ volatile("rdtsc" : "=a" (eax), "=d" (edx));
    /*ret 2 pipe binaries till left shift 32*/
	ret2  = ((unsigned long long)eax) | (((unsigned long long)edx) << 32);
	return ret2 - ret;
}
int rdtsc_check() {
	int i;
    /*average starts 0*/
	unsigned long long average = 0;
	for (i = 0; i < 10; i++) {
        /*adds first rdtsc process*/
		average = average + rdtscd();
		Sleep(500);
	}
	average = average / 10;
    /*returns false if average less than 750 true average 0*/
	return (average < 750 && average > 0) ? FALSE : TRUE;
}
int vmexit_check() {
	int i;
	unsigned long long average = 0;
	for (i = 0; i < 10; i++) {
        /*repeat process for vmexit checks*/
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







