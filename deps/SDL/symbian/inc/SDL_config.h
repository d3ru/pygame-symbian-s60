/*
    SDL - Simple DirectMedia Layer

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public
    License along with this library; if not, write to the Free Software
    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


*/

#ifndef _SDL_config_h
#define _SDL_config_h

#include "SDL_platform.h"

/* Add any platform that doesn't build using the configure system */
#if defined(__AMIGA__)
#include "SDL_config_amiga.h"
#elif defined(__DREAMCAST__)
#include "SDL_config_dreamcast.h"
#elif defined(__MACOS__)
#include "SDL_config_macos.h"
#elif defined(__MACOSX__)
#include "SDL_config_macosx.h"
#elif defined(__SYMBIAN32__)
#include "SDL_config_symbian.h" //must be before win32!
#elif defined(__WIN32__)
#include "SDL_config_win32.h"
#elif defined(__OS2__)
#include "SDL_config_os2.h"
#else
#include "SDL_config_minimal.h"
#endif /* platform config */

#endif /* _SDL_config_h */
