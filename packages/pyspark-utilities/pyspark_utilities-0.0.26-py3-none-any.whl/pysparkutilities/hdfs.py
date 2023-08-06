from .datastorage import DataStorage


class Hdfs(DataStorage):

    # overriding abstract method
    def load_dataset(self, read_all=True, input_dest='', header=True):

        if input_dest == '':
            input_dataset = self.args["input-dataset"]
        else:
            input_dataset = input_dest
        hdfs_host = self.args["hdfsHost-input-dataset"]
        hdfs_port = self.args["hdfsPort-input-dataset"]
        delimiter = self.args["delimiter"] if "delimiter" in self.args else ","
        input_file_format = self.args["inputFileFormat"] if "inputFileFormat" in self.args else "csv"
        input_columns = self.args["input-columns"] if "input-columns" in self.args else "*"
        columns_list = input_columns.split(",")

        if read_all is True:
            return self.spark.read.load("hdfs://"+hdfs_host+":"+hdfs_port+input_dataset, format=input_file_format, sep=delimiter, inferSchema=True, header=header, error_bad_lines=False)
        else:
            return self.spark.read.load("hdfs://"+hdfs_host+":"+hdfs_port+input_dataset, format=input_file_format, sep=delimiter, inferSchema=True, header=header, error_bad_lines=False).select(*columns_list)

    # overriding abstract method
    def save_dataset(self, df, output_dest):

        if output_dest == '':
            output_dataset = self.args["output-dataset"]
        else:
            output_dataset = output_dest
        delimiter = self.args["delimiter"] if "delimiter" in self.args else ","
        output_file_format = self.args["outputFileFormat"] if "outputFileFormat" in self.args else "csv"

        df.write.options(delimiter=delimiter).\
            mode('overwrite').\
            option("header", True).\
            save("hdfs://"+self.args["hdfsHost-output-dataset"]+":"+self.args["hdfsPort-output-dataset"]+output_dataset, format=output_file_format)
