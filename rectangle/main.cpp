#pragma comment(linker,"/STACK:64000000")
#define _CRT_SECURE_NO_WARNINGS
#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <cmath>
#include <map>
#include <set>
#include <ctime>
#include <algorithm>
#include <memory.h>
#include <stdio.h>
#include <stdlib.h>

using namespace std;

#define WR printf
#define RE scanf
#define PB push_back
#define SE second
#define FI first

#define FOR(i,k,n) for(int i=(k); i<=(n); i++)
#define DFOR(i,k,n) for(int i=(k); i>=(n); i--)
#define SZ(a) (int)((a).size())
#define FA(i,v) FOR(i,0,SZ(v)-1)
#define RFA(i,v) DFOR(i,SZ(v)-1,0)
#define CLR(a) memset(a, 0, sizeof(a))

#define LL long long
#define VI  vector<int>
#define PAR pair<int ,int>
#define o_O 1000000000

void __never(int a){printf("\nOPS %d", a);}
#define ass(s) {if (!(s)) {__never(__LINE__);cout.flush();cerr.flush();abort();}}

double eps = 0.000001;
double DX, DY;

int gcd( int x, int y )
{
	if (x<0) x=-x;
	if (y<0) y=-y;
	while (x&&y) x>y ? x%=y : y%=x;
	return x+y;
}

void printx( int a, int b )
{
	int g = gcd( a, b );
	a /= g; b /= g;
	if (b<0)
	{
		a = -a;
		b = -b;
	}
	if (b==1) cout << a;
	else cout << a << "/" << b;
}

void sol()
{
	int A, B, C, D;
	FOR(a,1,1000) FOR(b,1,1000) if ( fabs((double)a/b-DX) < eps )
	{
		A = a;
		B = b;
		break;
	}
	FOR(a,1,1000) FOR(b,1,1000) if ( fabs((double)a/b-DY) < eps )
	{
		C = a;
		D = b;
		break;
	}

	A = 14; B = 131; C = 17; D = 245;

	vector< pair< PAR, PAR > > coord1, coord2;
	int ddx = (B+A-1)/A, ddy = (D+C-1)/C;
	map< int, int > Map;
	for (int i=0; i < ddx; i++)
		for (int j=0; j < ddy; j++)
		{
			//cout << 4 << " " << i*(ddy+1)+j << " " << (i+1)*(ddy+1)+j << " "
			//	<< (i+1)*(ddy+1)+j+1 << " " << i*(ddy+1)+j+1 << "\n";
			Map[i*(ddy+1)+j]++;
			Map[(i+1)*(ddy+1)+j]++;
			Map[(i+1)*(ddy+1)+j+1]++;
			Map[i*(ddy+1)+j+1]++;
		}
	vector< PAR > vv;
	for ( map< int, int >::iterator it = Map.begin(); it != Map.end(); it++ )
		vv.push_back( make_pair( it->second, it->first ) );
	sort( vv.begin(), vv.end() );
	reverse( vv.begin(), vv.end() );
	Map.clear();
	map< int, int > iMap;
	FA(a,vv)
	{
		//cout << "[" << vv[a].second << " " << a << "] ";
		Map[vv[a].second] = a;
		iMap[a] = vv[a].second;
	}
	for (int i=0; i < ddx+1; i++)
		for (int j=0; j < ddy+1; j++)
		{
			coord1.push_back( make_pair( make_pair( min(B, i*A), B ), make_pair( min(D, j*C), D ) ) );
		}

	for (int i=0; i < ddx+1; i++)
		for (int j=0; j < ddy+1; j++)
		{
			coord2.push_back( make_pair(
				make_pair( ( i==ddx ? ((i&1) ? B%A : A-B%A) : ((i&1) ? A : 0) ), B ),
				make_pair( ( j==ddy ? ((j&1) ? D%C : C-D%C) : ((j&1) ? C : 0) ), D ) ) );
		}



	cout << (ddx+1) * (ddy+1) << "\n";
	FOR(a,0,SZ(Map)-1)
	{
		pair< PAR, PAR > pp = coord1[iMap[a]];
		printx( pp.FI.FI, pp.FI.SE );
		cout << ",";
		printx( pp.SE.FI, pp.SE.SE );
		cout << "\n";
	}
	cout << ddx * ddy << "\n";
	for (int i=0; i < ddx; i++)
		for (int j=0; j < ddy; j++)
		{
			//cout << 4 << " " << i*(ddy+1)+j << " " << (i+1)*(ddy+1)+j << " "
			//	<< (i+1)*(ddy+1)+j+1 << " " << i*(ddy+1)+j+1 << "\n";
			cout << 4 << " ";
			cout << Map[i*(ddy+1)+j] << " ";
			cout << Map[(i+1)*(ddy+1)+j] << " ";
			cout << Map[(i+1)*(ddy+1)+j+1] << " ";
			cout << Map[i*(ddy+1)+j+1] << "\n";
		}
	FOR(a,0,SZ(Map)-1)
	{
		pair< PAR, PAR > pp = coord2[iMap[a]];
		printx( pp.FI.FI, pp.FI.SE );
		cout << ",";
		printx( pp.SE.FI, pp.SE.SE );
		cout << "\n";
	}

	cout << "\n";
}

int main()
{
	freopen( "input.txt", "r", stdin );
	freopen( "output.txt", "w", stdout );

	int cnt = 0;
	char str[1000];
	while (gets(str))
	{
		for (int i=0; str[i]; i++)
			if (str[i]!=' ')
				cnt++;
	}
	cerr << cnt << "\n";

	//DX = 0.14; //maxx - minx;
	//DY = 0.065; //maxy - miny;

	sol();


	/*FOR(a,1,100) if (a==10) //if (a==8 || a==9 || a==10 || a==36)
	{
		cerr << a << "\n";
		char ch[100];
		sprintf( ch, "../data/problems/%d.ind", a );
		freopen( ch, "r", stdin );

		sprintf( ch, "../data/solutions/solution_%d_rectangle_3.out", a );
		freopen( ch, "w", stdout );

		int n;
		cin >> n;
		//ass( n==4 );
		double minx = 100., maxx = -100., miny = 100., maxy = -100;
		FOR(b,0,n-1)
		{
			double x, y;
			cin >> x >> y;
			minx = min( minx, x );
			maxx = max( maxx, x );
			miny = min( miny, y );
			maxy = max( maxy, y );
		}

		DX = maxx - minx;
		DY = maxy - miny;

		sol();
	}*/

	
	return 0;
}
