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

#include "system.h"

using namespace std;
using namespace PlatBox;

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

double eps = 0.00000001;

int n, m;
double X[1005], Y[1005];
VI E[1005];
bool can[1005][100][100];
bool can2[1005][100][100];
bool canbe[1005];
vector< VI > paths;
vector< int > factor;
int cur_p[1005], c_sz = 0;
double pi = acos(-1.);
double pi2 = pi*0.5;

int T = 10000;
int P = 10000;
int Strip = -1;

bool debug = true;

bool F[1005];

double get_dist( int i, int j )
{
	double dx = X[i]-X[j], dy = Y[i]-Y[j];
	return sqrt( dx*dx + dy*dy );
}

double get_angle( int i, int j, int k )
{
	double dx1 = X[i]-X[j], dx2 = X[k]-X[j];
	double dy1 = Y[i]-Y[j], dy2 = Y[k]-Y[j];

	double a1 = atan2( dy1, dx1 );
	double a2 = atan2( dy2, dx2 );
	double ang = max(a1,a2)-min(a1,a2);
	ang = min( ang, pi*2-ang );
	ass( -eps < ang && ang < pi+eps );
	return ang;
}

void p_search( double L )
{
	for (int z=1; z<=50; z++)
		if ( fabs(L-1./z) < eps )
		{
			if (canbe[cur_p[c_sz-1]])
			{
				VI v;
				FOR(a,0,c_sz-1) v.push_back( cur_p[a] );
				paths.push_back( v );
				factor.push_back( z );
			}
		}
	if ( L > 1.-eps ) return;

	if (clock() > T) exit(1);
	if (SZ(paths) > P) exit(2);

	int v = cur_p[c_sz-1];
	int pre = cur_p[c_sz-2];
	FOR(a,0,SZ(E[v])-1)
		if (E[v][a]==pre)
		{
			pre = a;
			break;
		}

	FOR(a,0,SZ(E[v])-1)
		if (can[v][pre][a])
		{
			cur_p[c_sz++] = E[v][a];
			p_search( L + get_dist( v, E[v][a] ) );
			c_sz--;
		}
}

void dfs( int v, int i, int j, double A )
{
	if ( fabs(A-pi)<eps )
	{
		can[v][i][j] = true;
		return;
	}
	if ( A > pi ) return;

	if (clock() > T) exit(1);

	int p1 = (j+1)%SZ(E[v]);
	int p2 = (j+SZ(E[v])-1)%SZ(E[v]);
	double ang = get_angle( E[v][j], v, E[v][p1] );
	if (ang > eps) dfs( v, i, p1, A + ang );
	ang = get_angle( E[v][j], v, E[v][p2] );
	if (ang > eps) dfs( v, i, p2, A + ang );
}

void dfs2( int v, int i, int j, double A )
{
	if ( fabs(A-pi2)<eps )
	{
		can2[v][i][j] = true;
		canbe[v] = true;
		return;
	}
	if ( A > pi2 ) return;

	if (clock() > T) exit(1);

	int p1 = (j+1)%SZ(E[v]);
	int p2 = (j+SZ(E[v])-1)%SZ(E[v]);
	double ang = get_angle( E[v][j], v, E[v][p1] );
	if (ang > eps) dfs2( v, i, p1, A + ang );
	ang = get_angle( E[v][j], v, E[v][p2] );
	if (ang > eps) dfs2( v, i, p2, A + ang );
}

bool p_next( VI & v1, VI & v2 )
{
	int u = v1[SZ(v1)-1];
	int pre = v1[SZ(v1)-2];
	if (u != v2[0]) return false;
	int ii = -1, jj = -1;
	FA(a,E[u]) if (E[u][a]==pre) { ii=a; break; }
	FA(a,E[u]) if (E[u][a]==v2[1]) { jj=a; break; }
	if (ii==-1 || jj==-1) return false;
	return can2[u][ii][jj];
}

void sort_them()
{
	FOR(a,0,n-1)
	{
		vector< pair< double, int > > V;
		FA(b,E[a]) V.push_back( make_pair( atan2( Y[E[a][b]]-Y[a], X[E[a][b]]-X[a] ), E[a][b] ) );
		sort( V.begin(), V.end() );
		FA(b,V) E[a][b] = V[b].SE;
	}
}

void sol()
{
	sort_them();

	CLR( can );
	CLR( can2 );
	CLR( canbe );
	FOR(a,0,n-1) FOR(b,0,SZ(E[a])-1)
	{
		dfs( a, b, b, 0. );
		dfs2( a, b, b, 0. );
	}

	if (debug) cerr << "Can phase finished\n";

	FOR(a,0,n-1) if (canbe[a])
		FA(b,E[a])
		{
			cur_p[0] = a;
			cur_p[1] = E[a][b];
			c_sz = 2;
			p_search( get_dist( a, E[a][b] ) );
		}

	if (debug) cerr << "Paths found " << SZ(paths) << "\n";
	cout << SZ(paths) << "\n";
	FA(a,paths)
	{
		cout << SZ(paths[a]) << "  ";
		FA(b,paths[a]) cout << paths[a][b] << " ";
		cout << "\n";
	}

	map< vector< VI >, VI > Map;
	DFOR(z,(Strip==-1?50:Strip),(Strip==-1?1:Strip))
	{
		FA(a,paths) if (factor[a]==z) FA(b,paths) if (factor[b]==1)
			if (p_next( paths[a], paths[b] ))
				FA(c,paths) if (factor[c]==z) if (p_next( paths[b], paths[c] ))
					FA(d,paths) if (factor[d]==1) if (p_next( paths[c], paths[d] ))
						if (p_next( paths[d], paths[a] ))
						{
							if (clock() > T) exit(1);

							//cout << a << " " << b << " " << c << " " << d << "\n";
							VI ind = VI(4);
							ind[0] = a; ind[1] = b; ind[2] = c; ind[3] = d;
							vector< VI > mi;
							FOR(e,0,3) mi.push_back( paths[ind[e]] );

							FOR(e,0,3)
							{
								vector< VI > vv;
								FOR(f,0,3) vv.push_back( paths[ind[(e+f)%4]] );
								if (vv < mi) mi = vv;
								vv.clear();
								DFOR(f,3,0)
								{
									VI v = paths[ind[(e+f)%4]];
									reverse( v.begin(), v.end() );
									vv.push_back( v );
								}
								if (vv < mi) mi = vv;
							}

							if (Map.find( mi ) == Map.end())
								Map[ mi ] = ind;
						}
	}

	if (SZ( Map )==0) exit(3);

	cout << "\n";
	cout << SZ( Map ) << "\n";
	cout << "\n";
	for ( map< vector< VI >, VI >::iterator it = Map.begin(); it != Map.end(); it++ )
	{
		CLR(F);
		VI vec;
		FOR(a,0,3) FA(b,it->first[a])
		{
			F[it->first[a][b]] = true;
			if (b) vec.push_back( it->first[a][b] );
		}

		map< int, set< int > > S;
		
		vec.push_back( vec[0] );
		vec.push_back( vec[1] );

		FA(a,vec) if (a && a!=SZ(vec)-1)
			if (SZ(E[vec[a]])==3)
				FA(b,E[vec[a]]) if (E[vec[a]][b]!=vec[a-1] && E[vec[a]][b]!=vec[a+1])
				{
					int ii = vec[a], jj = b;
					while(1)
					{
						if (!F[E[ii][jj]])
						{
							//Set.insert( make_pair( E[ii][jj], vec[a] ) );
							S[E[ii][jj]].insert( vec[a] );
							break;
						}
						int pre = 0;
						FA(c,E[E[ii][jj]]) if (E[E[ii][jj]][c]==ii)
						{
							pre = c;
							break;
						}
						bool flag = false;
						FA(c,E[E[ii][jj]]) //if (can[E[ii][jj]][pre][c])
							if ( fabs(get_angle( E[E[ii][jj]][pre], E[ii][jj], E[E[ii][jj]][c] )-pi) < eps )
							{
								flag = true;
								ii = E[ii][jj];
								jj = c;
								break;
							}
						if (!flag) break;
					}
				}

		bool megaflag = true;

		//if (SZ(S)==0) megafrag = false;
		for (map< int, set< int > >::iterator it2 = S.begin(); it2 != S.end(); it2++)
		{
			set< int > ss = it2->second;
			if (SZ(ss)<2) megaflag = false;
		}

		//if (megaflag)
		{
			FA(a,it->second) cout << it->second[a] << " ";
			cout << "\n";

			cout << SZ(S) << "\n";
			for (map< int, set< int > >::iterator it2 = S.begin(); it2 != S.end(); it2++)
			{
				set< int > ss = it2->second;
				cout << it2->first << " " << SZ(ss) << "  ";
				//ass( SZ(ss)>=2 );
				for (set< int >::iterator it3 = ss.begin(); it3 != ss.end(); it3++)
					cout << (*it3) << " ";
				//FA(a,vec) cout << vec[a] << " ";
				cout << "\n";
			}

			cout << "\n";
		}
	}

	cout << "-1 -1 -1 -1\n";

	/*FOR(a,0,n-1) FA(b,E[a]) FA(c,E[a])
		if (can[a][b][c])
			cout << a << ": " << E[a][b] << "-" << E[a][c] << "\n";*/
}

int main(int argc, char** argv)
{
	System::ParseArgs(argc, argv);

	int a = 28;
	//FOR(a,98,101) if (a!=24 && a!=30 && a!=32 && a!=33 && a!=83 && a!=84 && a!=85 && a!=86 && a!=88 &&
	//	a!=89 && a!=90 && a!=92 && a!=101)
	//	if (!(11<=a && a<=16) && !(38<=a && a<=44) && a!=46 && a!=47 && a!=53 && a!=54)
	
	{
		//cerr << a << "\n";

		if (System::HasArg("help"))
		{
			cout << "  in  - input file\n"
				<<  "  out - output file\n"
				<<  "  t   - time limit (default " << T << ")\n"
				<<  "  p   - limit for number of paths (default " << P << ")\n"
				<<  "  s   - limit for strip\n";
			cout << "Exit(1) = Time Limit Exceeded\n";
			cout << "Exit(2) = Paths Limit Exceeded\n";
			cout << "Exit(3) = No borders found\n";
			return 0;
		}

		if (System::HasArg("in"))
		{
			string inf = System::GetArgValue("in");
			freopen( inf.c_str(), "r", stdin );
			debug = false;
		}
		else
		{
			char ch[100];
			sprintf( ch, "../data/problems/%d.ind", a );
			freopen( ch, "r", stdin );
		}

		if (System::HasArg("out"))
		{
			string outf = System::GetArgValue("out");
			freopen( outf.c_str(), "w", stdout );
			debug = false;
		}
		else
		{
			//sprintf( ch, "../data/problems/%d.p", a );
			//freopen( ch, "w", stdout );
			freopen( "output.txt", "w", stdout );
		}

		if (System::HasArg("t"))
		{
			T = atoi(System::GetArgValue("t").c_str());
		}
		if (System::HasArg("p"))
		{
			P = atoi(System::GetArgValue("p").c_str());
		}
		if (System::HasArg("s"))
		{
			Strip = atoi(System::GetArgValue("s").c_str());
		}

		paths.clear();
		factor.clear();

		cin >> n;
		ass( n <= 1000 );
		FOR(z,0,n-1) E[z].clear();
		FOR(z,0,n-1) cin >> X[z] >> Y[z];
		cin >> m;
		FOR(z,1,m)
		{
			int x, y;
			cin >> x >> y;
			E[x].push_back( y );
			E[y].push_back( x );
			ass( SZ(E[x])<100 && SZ(E[y])<100 );
		}
		sol();
	}

	return 0;
}
