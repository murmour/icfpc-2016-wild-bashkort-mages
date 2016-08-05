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

double eps = 0.000000001;

int n, m;
double X[1005], Y[1005];
VI E[1005];
bool can[1005][100][100];
bool can2[1005][100][100];
bool canbe[1005];
vector< VI > paths;
int cur_p[1005], c_sz = 0;
double pi = acos(-1.);
double pi2 = pi*0.5;

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
	if ( fabs(L-1.) < eps )
	{
		if (canbe[cur_p[c_sz-1]])
		{
			VI v;
			FOR(a,0,c_sz-1) v.push_back( cur_p[a] );
			paths.push_back( v );
		}
		return;
	}
	if ( L > 1. ) return;

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

void sol()
{
	CLR( can );
	CLR( can2 );
	CLR( canbe );
	FOR(a,0,n-1) FOR(b,0,SZ(E[a])-1)
	{
		dfs( a, b, b, 0. );
		dfs2( a, b, b, 0. );
	}

	FOR(a,0,n-1) if (canbe[a])
		FA(b,E[a])
		{
			cur_p[0] = a;
			cur_p[1] = E[a][b];
			c_sz = 2;
			p_search( get_dist( a, E[a][b] ) );
		}

	cout << SZ(paths) << "\n";
	FA(a,paths)
	{
		cout << SZ(paths[a]) << "  ";
		FA(b,paths[a]) cout << paths[a][b] << " ";
		cout << "\n";
	}

	map< vector< VI >, VI > Map;
	FA(a,paths) FA(b,paths) if (p_next( paths[a], paths[b] ))
		FA(c,paths) if (p_next( paths[b], paths[c] ))
			FA(d,paths) if (p_next( paths[c], paths[d] ))
				if (p_next( paths[d], paths[a] ))
				{
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

	cout << SZ( Map ) << "\n";
	for ( map< vector< VI >, VI >::iterator it = Map.begin(); it != Map.end(); it++ )
	{
		FA(a,it->second) cout << it->second[a] << " ";
		cout << "\n";
	}

	//FOR(a,0,n-1) FA(b,E[a]) FA(c,E[a])
	//	if (can2[a][b][c])
	//		cout << a << ": " << E[a][b] << "-" << E[a][c] << "\n";
}

int main()
{
	FOR(a,1,101) if (a!=24 && a!=30 && a!=32 && a!=33 && a!=83 && a!=84 && a!=85 && a!=86 && a!=88 &&
		a!=89 && a!=90 && a!=92 && a!=101)
	{
		cerr << a << "\n";
		char ch[100];
		sprintf( ch, "../data/problems/%d.ind", a );
		freopen( ch, "r", stdin );

		sprintf( ch, "../data/problems/%d.p", a );
		freopen( ch, "w", stdout );

		paths.clear();

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
