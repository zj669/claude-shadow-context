/**
 * Template Loader
 * 模板加载器 - 从源目录读取模板文件
 */
/**
 * 获取模板目录的绝对路径
 */
export declare function getTemplatesDir(): string;
/**
 * 获取 Claude 模板目录的绝对路径
 */
export declare function getClaudeTemplatesDir(): string;
/**
 * 加载模板文件内容
 */
export declare function loadTemplate(relativePath: string): string;
/**
 * 获取模板目录下的所有文件
 */
export declare function listTemplates(dir?: string): string[];
/**
 * 检查模板文件是否存在
 */
export declare function templateExists(relativePath: string): boolean;
/**
 * 获取模板文件的绝对路径
 */
export declare function getTemplatePath(relativePath: string): string;
