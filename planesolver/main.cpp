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
	//freopen("input.txt","r",stdin);
	//freopen("output.txt","w",stdout);

	FOR(A,1020,3000) if ((1020<=A && A<=1031) || (2625<=A && A<=2627) || (2629<=A && A<=2631))
	{
		char ch[100];
		sprintf( ch, "../data/problems/%d.in", A );
		freopen( ch, "r", stdin );

		sprintf( ch, "../data/solutions/solution_%d_plane_4.out", A );
		freopen( ch, "w", stdout );
		//freopen( "output.txt", "w", stdout );

		ind = 0;

		int n;
		cin >> n;
		ass( n==1 );
		cin >> n;
		ass( n==8 );
		//FOR(a,0,7)
		//	V[a] = read_t();

		//FOR(a,0,7) cout << get_dist( V[a], V[(a+1)%8] ) << "\n";

		V[8] = read_t();
		V[10] = read_t();
		V[9] = read_t();
		V[7] = read_t();
		V[6] = read_t();
		V[1] = read_t();
		V[4] = read_t();
		V[0] = read_t();

		V[2] = make_pair( norm( V[0].FI.FI*V[4].FI.SE+V[4].FI.FI*V[0].FI.SE, V[0].FI.SE*V[4].FI.SE*2 ),
						norm( V[0].SE.FI*V[4].SE.SE+V[4].SE.FI*V[0].SE.SE, V[0].SE.SE*V[4].SE.SE*2 ) );
		V[3] = make_pair( norm( 2*V[0].FI.FI*V[8].FI.SE+V[8].FI.FI*V[0].FI.SE, V[0].FI.SE*V[8].FI.SE*3 ),
						norm( 2*V[0].SE.FI*V[8].SE.SE+V[8].SE.FI*V[0].SE.SE, V[0].SE.SE*V[8].SE.SE*3 ) );
		V[5] = make_pair( norm( V[0].FI.FI*V[8].FI.SE+2*V[8].FI.FI*V[0].FI.SE, V[0].FI.SE*V[8].FI.SE*3 ),
						norm( V[0].SE.FI*V[8].SE.SE+2*V[8].SE.FI*V[0].SE.SE, V[0].SE.SE*V[8].SE.SE*3 ) );

		//FOR(a,0,10) cout << get_dist( V[a], V[(a+1)%11] ) << "\n";

		/*cout << get_dist( V[0], V[2] ) << "\n";
		cout << get_dist( V[2], V[4] ) << "\n";
		cout << get_dist( V[4], V[1] ) << "\n";
		cout << get_dist( V[1], V[6] ) << "\n";
		cout << get_dist( V[6], V[7] ) << "\n";
		cout << get_dist( V[7], V[9] ) << "\n";
		cout << get_dist( V[9], V[10] ) << "\n";
		cout << get_dist( V[10], V[8] ) << "\n";
		cout << get_dist( V[8], V[5] ) << "\n";
		cout << get_dist( V[5], V[3] ) << "\n";
		cout << get_dist( V[3], V[0] ) << "\n";*/

		w( 0, 6, 0, 6, 0 );
		w( 0, 6, 2, 6, 5 );
		w( 0, 6, 3, 6, 7 );
		w( 0, 6, 4, 6, 5 );
		w( 0, 6, 5, 6, 7 );
		w( 0, 6, 6, 6, 1 );

		w( 1, 6, 4, 6, 3 );
		w( 1, 6, 6, 6, 6 );

		w( 2, 6, 0, 6, 4 );
		w( 2, 6, 2, 6, 0 );
		w( 2, 6, 3, 6, 2 );
		w( 2, 6, 5, 6, 7 );
		w( 2, 6, 6, 6, 1 );

		w( 3, 6, 4, 6, 3 );
		w( 3, 6, 6, 6, 6 );

		w( 4, 6, 0, 6, 0 );
		w( 4, 6, 2, 6, 5 );

		w( 5, 6, 0, 6, 2 );
		w( 5, 6, 3, 6, 9 );
		w( 5, 6, 4, 6, 8 );
		w( 5, 6, 6, 6, 3 );

		w( 11, 12, 7, 12, 10 );

		w( 6, 6, 0, 6, 1 );
		w( 6, 6, 1, 6, 3 );
		w( 6, 6, 3, 6, 8 );
		w( 6, 6, 4, 6, 9 );
		w( 6, 6, 6, 6, 1 );


		cout << ind << "\n";
		FOR(a,0,ind-1) wri( Z[a] );

		cout << "23\n";
		cout << "3 0 1 8\n";
		cout << "3 1 9 8\n";
		cout << "4 1 2 10 9\n";
		cout << "4 2 3 6 10\n";
		cout << "4 3 4 7 6\n";
		cout << "3 4 5 7\n";
		cout << "3 6 11 10\n";
		cout << "3 6 7 11\n";
		cout << "3 7 12 11\n";
		cout << "3 8 9 16\n";
		cout << "3 8 16 15\n";
		cout << "4 9 10 18 16\n";
		cout << "3 10 11 13\n";
		cout << "3 11 14 13\n";
		cout << "3 11 12 14\n";
		cout << "5 10 13 19 21 18\n";
		cout << "3 13 14 19\n";
		cout << "3 14 20 19\n";
		cout << "4 15 16 18 17\n";
		cout << "3 17 23 22\n";
		cout << "5 17 18 21 24 23\n";
		cout << "5 21 19 20 26 25\n";
		cout << "3 21 25 24\n";

		FOR(a,0,ind-1) wri( V[T[a]] );
	}

	return 0;
}
