/* Copyright (C) 2007 Harry Li  All Rights Reserved.
 *
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this software; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307,
 * USA.
 */

//  Include Files  

#include <ft2build.h>
#include FT_FREETYPE_H

//#include <sys/reent.h>
#include <gdi.h>
#include <fbs.h>

#include "libsft2.h"	// CSymbianFreeType
#include "libsft2.pan"	// panic codes
#include "debug.h"
#define LOGFN "c:\\libsft2.log"
//  Member Functions

EXPORT_C TVersion CSymbianFreeType::Version() const
	{
	// Version number of example API
	const TInt KMajor = 0;
	const TInt KMinor = 0;
	const TInt KBuild = 1;
	return TVersion(KMajor, KMinor, KBuild);
	}

EXPORT_C CSymbianFreeType* CSymbianFreeType::NewLC()
	{
	CSymbianFreeType* self = new (ELeave) CSymbianFreeType;
	CleanupStack::PushL(self);
	self->ConstructL();
	return self;
	}

EXPORT_C CSymbianFreeType* CSymbianFreeType::NewL()
	{
	CSymbianFreeType* self = CSymbianFreeType::NewLC();
	CleanupStack::Pop(self);
	return self;
	}

CSymbianFreeType::CSymbianFreeType ()
// note, CBase initialises all member variables to zero
	{
	}

void CSymbianFreeType::ConstructL ()
	{
	// second phase constructor, anything that may leave must be constructed here
	TInt error;
	error = FT_Init_FreeType (&iLibrary);
	iFace = NULL;
	}

EXPORT_C CSymbianFreeType::~CSymbianFreeType()
	{
	if (iFace)
	FT_Done_Face(iFace);
	FT_Done_FreeType(iLibrary);
	//CloseSTDLIB();
	}

EXPORT_C void CSymbianFreeType::SetFontColor(TRgb aColor, TRgb aBackColor)
	{
	iColor = aColor;
	iBackColor = aBackColor;
	}

EXPORT_C void CSymbianFreeType::DrawString(CGraphicsContext& aGc, TPoint aPoint, const TDesC& aDes)
	{
	int error, glyph_index;
	int sh=aGc.Device()->SizeInPixels().iHeight;
	int sw=aGc.Device()->SizeInPixels().iWidth;
	int i,w,h,x,y,flvl,ilvl;/*iterator, width, height, x, y, font_level, invert_level*/
	unsigned char* sample;
	FT_GlyphSlot slot;
	TPoint point(aPoint);

	ilvl = User::NTickCount();
	for (i=0; i<aDes.Length(); i++)
		{
		glyph_index = FT_Get_Char_Index( iFace, aDes[i] );
		error = FT_Load_Glyph(
				iFace, /* handle to face object */
				glyph_index, /* glyph index */
				FT_LOAD_DEFAULT );

		error = FT_Render_Glyph( iFace->glyph, FT_RENDER_MODE_NORMAL );

		slot = iFace->glyph;

		w = slot->bitmap.width;
		h = slot->bitmap.rows;
		sample = slot->bitmap.buffer;
		point.iX += slot->bitmap_left;
		point.iY = aPoint.iY-slot->bitmap_top;

		for (y=0; y<h; y++)
			{
			if (point.iY<sh && point.iY>=0)
				{
				for (x=0; x<w; x++)
					{
					point.iX++;
					if (point.iX>=sw || point.iX<0) continue;
					flvl = sample[y*w+x];
					ilvl = 0x100 - flvl;
					aGc.SetPenColor(TRgb((iColor.Red()*flvl+iBackColor.Red()*ilvl)>>8, (iColor.Green()*flvl+iBackColor.Green()*ilvl)>>8, (iColor.Blue()*flvl+iBackColor.Blue()*ilvl)>>8));
					aGc.Plot(point);
					}
				point.iX -= w;
				}
			point.iY++;
			}
		point.iX += (slot->advance.x>>6) - slot->bitmap_left;
		}

	LOGP((f, "Total Time Cost [%d] NanoTicks", User::NTickCount()-ilvl));
	}

EXPORT_C TBool CSymbianFreeType::InitializeFace(TDes8& aFileName, TUint32 aFontIndex, const CGraphicsDevice* aGd, TInt aSizeInPoint)
	{
	TInt error;
	TSize twipSize;
	TSize pixSize;

	if (iFace)
	FT_Done_Face(iFace);

	twipSize = aGd->SizeInTwips();
	pixSize = aGd->SizeInPixels();

	aFileName.ZeroTerminate();
	error = FT_New_Face( iLibrary, (const char*)(aFileName.Ptr()), aFontIndex, &iFace );
	if (error)
		{
		return EFalse;
		}

	iPPI.iWidth = pixSize.iWidth * 1440 / twipSize.iWidth;
	iPPI.iHeight = pixSize.iHeight * 1440 / twipSize.iHeight;
	error = FT_Set_Char_Size(
			iFace, /* handle to face object */
			0, /* char_width in 1/64th of points */
			aSizeInPoint*64, /* char_height in 1/64th of points */
			iPPI.iWidth, /* horizontal device resolution */
			iPPI.iHeight ); /* vertical device resolution */

	if (error)
		{
		return EFalse;
		}

	return ETrue;
	}

