#ifndef LCD_H
#define LCD_H

#include "Arduino.h"

#include "enums.h"

class Lcd {
    public:
        Lcd();
        void init();

        void draw_address(int address, e_number_base number_base);
        void draw_queued_address(char queued_address_str[]);
        void draw_data(int data, e_number_base number_base, e_sign_mode, sign_mode);
        void draw_queued_data(char queued_data_str[]);
        void draw_number_base_indicator(e_number_base number_base);
        void draw_sign_mode_indicator(e_sign_mode, sign_mode);
        void draw_address_update_mode_indicator(e_address_update_mode, address_update_mode);
        void draw_ram_region_indicator(e_ram_region, ram_region);
        void draw_run_mode_indicator(e_run_mode, run_mode);
        void draw_clock_frequency(float frequency);
        void draw_program_name(char program_name[]);

    private:
        void constructor_defaults();
}

#endif

// 12345678901234567890



// A: 0000111100001111
//    _
// D: 00001111 _
// DEC +/- PRG INC RUN


// ADDR   DATA  DEC +/-
//  123     34  PRG RUN
// ====   ====  INC 
// 12_    _     



// A: _        00001111
// D:-00001111-00001111
// 1: Program     2 KHz
// PRG DEC SIG INC  RUN


// 12345678901234567890
// A:  00001111 PRG INC
//  >  _        DEC SIG
// D: -00001111 RUN 
//  >  _        PRGNAME



// A:       240 PRG INC
//  >  104_     DEC SIG
// D:       -34 RUN   1
//  > -25_      PRGNAME