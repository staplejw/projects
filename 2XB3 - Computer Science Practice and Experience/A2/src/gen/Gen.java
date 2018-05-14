package gen;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.Writer;
import java.util.Random;
import java.util.UUID;

public class Gen {

	public static void main(String[] args) throws IOException {
		String studentId = "001052815";
		String folder = "data";

		int seed = 0;
		for (int i = 0; i < studentId.length(); i++) {
			seed += ((int) studentId.charAt(i)) * 10 ^ i;
		}

		Writer wr = null;
		try {
			File f = new File(folder + "\\a2_in.txt");
			wr = new BufferedWriter(new FileWriter(f));
			Random random = new Random(seed);

			for (int i = 0; i < 16; i++) {
				if (i > 0)
					wr.write(",");
				wr.write("{" + UUID.randomUUID() + ","
						+ random.nextInt(1024) + "," + random.nextInt(10) + "}");
			}
			wr.write("\r\n");
			
			for (int i = 0; i < 64; i++) {
				if (i > 0)
					wr.write(",");
				wr.write("{" + UUID.randomUUID() + ","
						+ random.nextInt(4096) +  "," + random.nextInt(50) +"}");
			}
			wr.write("\r\n");
			
			for (int i = 0; i < 256; i++) {
				if (i > 0)
					wr.write(",");
				wr.write("{" + UUID.randomUUID() + ","
						+ random.nextInt(16384) +  "," + random.nextInt(200) +"}");
			}
			wr.write("\r\n");	
			
			for (int i = 0; i < 1024; i++) {
				if (i > 0)
					wr.write(",");
				wr.write("{" + UUID.randomUUID() + ","
						+ random.nextInt(65536) +  "," + random.nextInt(1000) +"}");
			}
			wr.write("\r\n");

			for (int i = 0; i < 4096; i++) {
				if (i > 0)
					wr.write(",");
				wr.write("{" + UUID.randomUUID() + ","
						+ random.nextInt(1048576) +  "," + random.nextInt(5000) +"}");
			}
			wr.write("\r\n");
			
			for (int i = 0; i < 16384; i++) {
				if (i > 0)
					wr.write(",");
				wr.write("{" + UUID.randomUUID() + ","
						+ random.nextInt(1048576) +  "," + random.nextInt(20000) +"}");
			}
			wr.write("\r\n");
			
			for (int i = 0; i < 65536; i++) {
				if (i > 0)
					wr.write(",");
				wr.write("{" + UUID.randomUUID() + ","
						+ random.nextInt(1048576) +  "," + random.nextInt(20000) +"}");
			}
			wr.write("\r\n");
			
			for (int i = 0; i < 262144; i++) {
				if (i > 0)
					wr.write(",");
				wr.write("{" + UUID.randomUUID() + ","
						+ random.nextInt(1048576) +  "," + random.nextInt(20000) +"}");
			}
			wr.write("\r\n");
			
		} finally {
			if (wr != null)
				wr.close();
		}
	}

}
