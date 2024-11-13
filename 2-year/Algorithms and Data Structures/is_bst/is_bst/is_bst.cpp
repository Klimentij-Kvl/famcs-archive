#include <fstream>

using namespace std;

int main() {
	ifstream in("input.txt");
	ofstream out("output.txt");

	int n;
	in >> n;

	if (n == 0 || n == 1) {
		out << "YES";
		return 0;
	}

	int* val = new int[n];
	in >> val[0];

	long long* min_val = new long long[n];
	long long* max_val = new long long[n];
	min_val[0] = 0-9223372036854775808;
	max_val[0] = 9223372036854775807;

	int p;
	char c;
	for (int i = 1; i < n; i++) {
		in >> val[i] >> p >> c;
		if (c == 'L') {
			if (val[i] >= val[p-1]) {
				out << "NO";
				return 0;
			}
			min_val[i] = min_val[p-1];
			max_val[i] = val[p-1];
		}
		else if (c == 'R') {
			if (val[i] < val[p - 1]) {
				out << "NO";
				return 0;
			}
			min_val[i] = val[p-1];
			max_val[i] = max_val[p-1];
		}

		if (val[i] < min_val[i] || val[i] >= max_val[i]) {
			out << "NO";
			return 0;
		}
	}


	out << "YES";
	return 0;
}