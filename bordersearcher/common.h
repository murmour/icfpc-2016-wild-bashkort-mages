#ifndef __COMMON_H__
#define __COMMON_H__

#define INTERACTIVE_MODE

// uncomment to disable assertion checks
//#define NDEBUG
#include <assert.h>

#include <vector>
#include <string>
#include <algorithm>
#include <cmath>
#include <list>
#include <set>
#include <map>
#include <queue>
#include <string.h>
#include <iostream>

#undef min
#undef max

//#include "json/json.h"

//#include "log.h"

#ifdef INTERACTIVE_MODE
#define dassert(x)
#else
#define dassert(x) assert(x)
#endif

#define E_PB_OK                0
#define E_PB_FAIL              1

#define SAFE_DELETE(p)  { if(p) { delete (p); (p)=NULL; } }
#define SAFE_DELETE_ARR(p)  { if(p) { delete [] (p); (p)=NULL; } }
#define SAFE_RELEASE(p) { if(p) { (p)->Release(); (p)=NULL; } }

#define ensure_true(x) { bool __res = bool(x); assert(__res); }

#define DISALLOW_COPY_AND_ASSIGN(TypeName) \
  TypeName(const TypeName&);   \
  void operator=(const TypeName&)

#ifndef _MSC_VER
#define sprintf_s sprintf
#endif

inline int imin(int a, int b) { return std::min(a, b); }

typedef float f32;
typedef double f64;

typedef signed char i8;
typedef unsigned char u8;
typedef int i32;
typedef unsigned int u32;
typedef long long i64;

typedef u32 PBBOOL;

#define PBTRUE				1
#define PBFALSE				0

#define ANSI_CODEPAGE		1251

#define F32INF 1e38f
#define I32INF 0x7fffffff

#endif
