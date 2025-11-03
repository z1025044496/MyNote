# OpenCppCoverage

## 命令

* 仅支持命令行执行：
|命令|用法|
|---|---|
|-v [ --verbose ]|信息全输出|
|-q [ --quiet ]|仅输出告警|
|-h [ --help ]|使用说明|
|--config_file arg|按照配置文件执行|

* 可卸载配置文件中：
|命令|用法|
|---|---|
|--modules arg (=*)|指定统计的模块|
|--excluded_modules arg|排除不需要收集代码覆盖率的源代码文件或目录|
|--sources arg (=*)|指定要收集代码覆盖率的源|代码文件或目录|
|--excluded_sources arg|排除不需要收集代码覆盖率的源代码文件或目录（第三方库）|
|--input_coverage arg|本地统计合并其他统计结果，必须是二进制格式的|
|--export_type arg (=html)|格式：`<type>:<path>`输出统计报告格式和保存路径，默认`html`，可选`binary`、`cobertura `|
|--working_dir arg|程序运行时的工作目录|
|--cover_children|为子进程启用代码覆盖|
|--no_aggregate_by_file|别合并统计相同文件|
|-unified_diff arg|用来比较两次覆盖率运行的差异|
|--continue_after_cpp_exception||
|--optimized_build|支持优化生成（Visual Studio中的/O1或/O2）|
|--excluded_line_regex arg|此选项从源文件中排除与整个正则表达式匹配的所有行。例如，排除所有包含else的行: `--excluded_line_regex “.*else.*”`|
|--substitute_path arg|格式：`< pdbStartPath >?< localPath >`，解决pdb读取的路径和编译机器上不一致的问题|

