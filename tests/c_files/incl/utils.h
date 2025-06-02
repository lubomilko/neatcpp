#ifndef UTILS_H
#define UTILS_H

#define utl_LPRFX_S8_D                                  s8
#define utl_LPRFX_S16_D                                 s16
#define utl_LPRFX_S32_D                                 s32
#define utl_LPRFX_S64_D                                 s64
#define utl_LPRFX_UNS8_D                                u8
#define utl_LPRFX_UNS16_D                               u16
#define utl_LPRFX_UNS32_D                               u32
#define utl_LPRFX_UNS64_D                               u64

#define utl_UPRFX_S8_D                                  S8
#define utl_UPRFX_S16_D                                 S16
#define utl_UPRFX_S32_D                                 S32
#define utl_UPRFX_S64_D                                 S64
#define utl_UPRFX_UNS8_D                                U8
#define utl_UPRFX_UNS16_D                               U16
#define utl_UPRFX_UNS32_D                               U32
#define utl_UPRFX_UNS64_D                               U64

#define utl_HIGHER_TYPE_S8_D                            S16
#define utl_HIGHER_TYPE_S16_D                           S32
#define utl_HIGHER_TYPE_S32_D                           S64
#define utl_HIGHER_TYPE_UNS8_D                          UNS16
#define utl_HIGHER_TYPE_UNS16_D                         UNS32
#define utl_HIGHER_TYPE_UNS32_D                         UNS64


#define utl_LPRFX(TYPE)                                 utl_LPRFX_ ## TYPE ## _D

#define utl_UPRFX(TYPE)                                 utl_UPRFX_ ## TYPE ## _D

#define utl_HIGHER_TYPE(TYPE)                           utl_HIGHER_TYPE_ ## TYPE ## _D

#define utl_REF_MACRO_EXP_ARGS(MACRO_NAME, ...)         MACRO_NAME(__VA_ARGS__)


#endif /* #ifndef UTILS_H */
