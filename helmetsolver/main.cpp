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

pair< PAR, PAR > V[20];

pair< PAR, PAR > read_t()
{
	string str;
	cin >> str;
	FA(a,str) if (str[a]=='/' || str[a]==',') str[a] = ' ';
	int x, y, p, q;
	sscanf( str.c_str(), "%d%d%d%d", &x, &y, &p, &q );
	return make_pair( make_pair( x, y ), make_pair( p, q ) );
}

int gcd( int x, int y )
{
	if (x<0) x=-x;
	if (y<0) y=-y;
	while (x&&y) x>y ? x%=y : y%=x;
	return x+y;
}

PAR norm( int x, int y )
{
	int g = gcd( x, y );
	x /= g; y /= g;
	if (y<0)
	{
		x = -x;
		y = -y;
	}
	return make_pair( x, y );
}

double get_dist( pair< PAR, PAR > A, pair< PAR, PAR > B )
{
	double dx = (double)A.FI.FI/A.FI.SE - (double)B.FI.FI/B.FI.SE;
	double dy = (double)A.SE.FI/A.SE.SE - (double)B.SE.FI/B.SE.SE;
	//cerr << dx << " " << dy << "\n";
	return sqrt( dx*dx + dy*dy );
}

pair< PAR, PAR > Z[30];
int T[30];
int ind = 0;

void w( int x1, int x2, int y1, int y2, int t )
{
	Z[ind] = make_pair( norm( x1, x2 ), norm( y1, y2 ) );
	T[ind] = t;
	ind++;
}

void wri( pair< PAR, PAR > pp )
{
	PAR p = norm( pp.FI.FI, pp.FI.SE );
	PAR q = norm( pp.SE.FI, pp.SE.SE );

	cout << p.FI;
	if (p.SE!=1) cout << "/" << p.SE;
	cout << ",";
	cout << q.FI;
	if (q.SE!=1) cout << "/" << q.SE;
	cout << "\n";
}

int main()
{
	FOR(A,0,5000) if ((675<=A && A<=690) || (3031<=A && A<=3041) || (4117<=A && A<=4119))
	{
		char ch[100];
		sprintf( ch, "../data/problems/%d.in", A );
		if (!freopen( ch, "r", stdin )) continue;

		cerr << A << "\n";

		sprintf( ch, "../data/solutions/solution_%d_helmet_2.out", A );
		freopen( ch, "w", stdout );
		//freopen( "output.txt", "w", stdout );

		ind = 0;
		int n;
		cin >> n;
		ass( n==1 );
		cin >> n;
		ass( n==15 );
		FOR(a,0,14)
			V[a] = read_t();

		//FOR(a,0,14) cout << get_dist( V[a], V[(a+1)%15] ) << "\n";
		V[15] = make_pair( make_pair( 1, 2 ), make_pair( 0, 1 ) );

		w( 0, 1, 0, 1, 0 );
		w( 0, 1, V[14].FI.FI, V[14].FI.SE, 14 );
		w( 0, 1, V[4].FI.FI, V[14].FI.SE, 4 );
		w( 0, 1, 1, 1, 3 );

		w( V[14].FI.FI, V[14].FI.SE, 0, 1, 14 );
		w( V[14].FI.FI, V[14].FI.SE, 1, 1, 4 );

		w( 1, 2, 0, 1, 15 );
		w( 1, 2, 1, 2, 9 );
		w( 1, 2, 1, 1, 15 );

		w( V[12].FI.SE-V[12].FI.FI, V[12].FI.SE, V[12].FI.FI, V[12].FI.SE, 12 );
		w( V[12].FI.SE-V[12].FI.FI, V[12].FI.SE, V[12].FI.SE-V[12].FI.FI, V[12].FI.SE, 6 );

		w( 1, 1, 0, 1, 11 );
		w( 1, 1, 1, 2, 15 );
		w( 1, 1, 1, 1, 7 );

		cout << ind << "\n";
			FOR(a,0,ind-1) wri( Z[a] );

		cout << "14\n";
		cout << "3 7 6 4\n";
		cout << "3 7 4 0\n";
		cout << "3 7 0 1\n";
		cout << "3 7 1 2\n";
		cout << "3 7 2 3\n";
		cout << "3 7 3 5\n";
		cout << "3 7 5 8\n";

		cout << "3 7 8 10\n";
		cout << "4 7 10 12 9\n";
		cout << "3 7 9 6\n";

		cout << "3 6 9 11\n";
		cout << "3 9 12 11\n";

		cout << "3 8 13 10\n";
		cout << "3 10 13 12\n";

		FOR(a,0,ind-1) wri( V[T[a]] );
	}

	return 0;
}
