"""
conversion_functions.py (Windows专用版)
PPTX/ODP格式转换功能，支持子进程调用
专门为Windows平台优化，使用LibreOffice自带的Python解释器
"""
import uno # type: ignore
import sys, os
import argparse
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
from logger_config import get_logger, log_function_call, log_execution_time, setup_subprocess_logging

def convert_pptx_to_odp_pyuno(pptx_path, output_dir=None):
    """
    使用PyUNO接口将PPTX文件转换为ODP文件
    :param pptx_path: 输入的PPTX文件路径
    :param output_dir: 输出目录（默认为PPTX文件所在目录）
    :return: 转换后ODP文件路径，失败返回None
    """
    logger = get_logger("pyuno.subprocess")
    
    if not os.path.exists(pptx_path):
        logger.error(f"PPTX文件不存在: {pptx_path}")
        return None

    if output_dir is None:
        output_dir = os.path.dirname(pptx_path)

    try:
        logger.info(f"使用PyUNO接口转换PPTX到ODP: {pptx_path}")
        
        # 连接到LibreOffice
        localContext = uno.getComponentContext()
        resolver = localContext.ServiceManager.createInstanceWithContext(
            "com.sun.star.bridge.UnoUrlResolver", localContext)
        context = resolver.resolve(
            "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
        
        # 获取桌面服务
        desktop = context.ServiceManager.createInstanceWithContext(
            "com.sun.star.frame.Desktop", context)
        
        # 打开PPTX文件
        file_url = uno.systemPathToFileUrl(os.path.abspath(pptx_path))
        logger.debug(f"打开PPTX文件: {file_url}")
        
        # 加载文档时设置为隐藏模式
        props = []
        prop = uno.createUnoStruct('com.sun.star.beans.PropertyValue')
        prop.Name = "Hidden"
        prop.Value = True
        props.append(prop)
        
        presentation = desktop.loadComponentFromURL(file_url, "_blank", 0, tuple(props))
        
        if not presentation:
            logger.error("无法加载PPTX文件")
            return None
        
        # 生成ODP输出路径
        base_name = os.path.splitext(os.path.basename(pptx_path))[0]
        odp_path = os.path.join(output_dir, base_name + ".odp")
        output_url = uno.systemPathToFileUrl(os.path.abspath(odp_path))
        
        logger.debug(f"保存为ODP文件: {output_url}")
        
        # 设置保存参数为ODP格式
        save_props = []
        
        # 设置过滤器为ODP格式
        filter_prop = uno.createUnoStruct('com.sun.star.beans.PropertyValue')
        filter_prop.Name = "FilterName"
        filter_prop.Value = "impress8"  # ODP格式的过滤器名称
        save_props.append(filter_prop)
        
        # 设置覆盖已存在文件
        overwrite_prop = uno.createUnoStruct('com.sun.star.beans.PropertyValue')
        overwrite_prop.Name = "Overwrite"
        overwrite_prop.Value = True
        save_props.append(overwrite_prop)
        
        # 保存为ODP格式
        presentation.storeToURL(output_url, tuple(save_props))
        
        # 关闭文档
        presentation.close(True)
        
        # 验证文件是否创建成功
        if os.path.exists(odp_path):
            logger.info(f"✅ PPTX转ODP成功: {odp_path}")
            return odp_path
        else:
            logger.error("ODP文件保存失败，文件不存在")
            return None
            
    except Exception as e:
        logger.error(f"PyUNO转换PPTX到ODP时出错: {e}", exc_info=True)
        # 尝试关闭可能打开的文档
        try:
            if 'presentation' in locals() and presentation:
                presentation.close(True)
        except:
            pass
        return None

def convert_odp_to_pptx_pyuno(odp_path, output_dir=None):
    """
    使用PyUNO接口将ODP文件转换为PPTX文件
    :param odp_path: 输入的ODP文件路径
    :param output_dir: 输出目录（默认为ODP文件所在目录）
    :return: 转换后PPTX文件路径，失败返回None
    """
    logger = get_logger("pyuno.subprocess")
    
    if not os.path.exists(odp_path):
        logger.error(f"ODP文件不存在: {odp_path}")
        return None

    if output_dir is None:
        output_dir = os.path.dirname(odp_path)

    try:
        logger.info(f"使用PyUNO接口转换ODP到PPTX: {odp_path}")
        
        # 连接到LibreOffice
        localContext = uno.getComponentContext()
        resolver = localContext.ServiceManager.createInstanceWithContext(
            "com.sun.star.bridge.UnoUrlResolver", localContext)
        context = resolver.resolve(
            "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
        
        # 获取桌面服务
        desktop = context.ServiceManager.createInstanceWithContext(
            "com.sun.star.frame.Desktop", context)
        
        # 打开ODP文件
        file_url = uno.systemPathToFileUrl(os.path.abspath(odp_path))
        logger.debug(f"打开ODP文件: {file_url}")
        
        # 加载文档时设置为隐藏模式
        props = []
        prop = uno.createUnoStruct('com.sun.star.beans.PropertyValue')
        prop.Name = "Hidden"
        prop.Value = True
        props.append(prop)
        
        presentation = desktop.loadComponentFromURL(file_url, "_blank", 0, tuple(props))
        
        if not presentation:
            logger.error("无法加载ODP文件")
            return None
        
        # 生成PPTX输出路径
        base_name = os.path.splitext(os.path.basename(odp_path))[0]
        pptx_path = os.path.join(output_dir, base_name + ".pptx")
        output_url = uno.systemPathToFileUrl(os.path.abspath(pptx_path))
        
        logger.debug(f"保存为PPTX文件: {output_url}")
        
        # 设置保存参数为PPTX格式
        save_props = []
        
        # 设置过滤器为PPTX格式
        filter_prop = uno.createUnoStruct('com.sun.star.beans.PropertyValue')
        filter_prop.Name = "FilterName"
        filter_prop.Value = "Impress MS PowerPoint 2007 XML"  # PPTX格式的过滤器名称
        save_props.append(filter_prop)
        
        # 设置覆盖已存在文件
        overwrite_prop = uno.createUnoStruct('com.sun.star.beans.PropertyValue')
        overwrite_prop.Name = "Overwrite"
        overwrite_prop.Value = True
        save_props.append(overwrite_prop)
        
        # 保存为PPTX格式
        presentation.storeToURL(output_url, tuple(save_props))
        
        # 关闭文档
        presentation.close(True)
        
        # 验证文件是否创建成功
        if os.path.exists(pptx_path):
            logger.info(f"✅ ODP转PPTX成功: {pptx_path}")
            return pptx_path
        else:
            logger.error("PPTX文件保存失败，文件不存在")
            return None
            
    except Exception as e:
        logger.error(f"PyUNO转换ODP到PPTX时出错: {e}", exc_info=True)
        # 尝试关闭可能打开的文档
        try:
            if 'presentation' in locals() and presentation:
                presentation.close(True)
        except:
            pass
        return None

def main():
    """
    主程序入口 - 支持子进程调用
    """
    # 设置子进程日志
    current_dir = os.path.dirname(os.path.abspath(__file__))
    logs_dir = os.path.join(current_dir, "logs")
    
    # 确保logs目录存在
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    log_file = os.path.join(logs_dir, "conversion_functions_subprocess.log")
    logger = setup_subprocess_logging(log_file)
    
    logger.info("=" * 60)
    logger.info("启动conversion_functions子进程")
    logger.info("=" * 60)
    
    parser = argparse.ArgumentParser(description='PPTX/ODP格式转换工具')
    parser.add_argument('--mode', required=True, choices=['pptx2odp', 'odp2pptx'], 
                       help='转换模式：pptx2odp 或 odp2pptx')
    parser.add_argument('--input', required=True, help='输入文件路径')
    parser.add_argument('--output', required=True, help='输出文件路径')
    
    args = parser.parse_args()
    
    # 统一路径为绝对路径，避免cwd差异
    abs_input = os.path.abspath(args.input)
    abs_output = os.path.abspath(args.output)

    logger.info(f"转换模式: {args.mode}")
    logger.info(f"输入文件: {abs_input}")
    logger.info(f"输出文件: {abs_output}")
    
    # 检查输入文件是否存在
    if not os.path.exists(abs_input):
        logger.error(f"输入文件不存在: {abs_input}")
        return 1
    
    # 确保输出目录存在
    output_dir = os.path.dirname(abs_output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logger.debug(f"创建输出目录: {output_dir}")
    
    try:
        if args.mode == 'pptx2odp':
            result_path = convert_pptx_to_odp_pyuno(abs_input, output_dir)
        elif args.mode == 'odp2pptx':
            result_path = convert_odp_to_pptx_pyuno(abs_input, output_dir)
        else:
            logger.error(f"不支持的转换模式: {args.mode}")
            return 1
        
        if result_path:
            # 如果输出路径与指定路径不同，重命名
            if result_path != abs_output:
                os.rename(result_path, abs_output)
                logger.info(f"重命名输出文件: {abs_output}")
            
            logger.info(f"✅ 转换成功: {args.output}")
            
            # 输出结果到标准输出（供主进程读取）
            result = {
                'success': True,
                'output_path': abs_output,
                'input_path': abs_input,
                'mode': args.mode
            }
            print(json.dumps(result))
            return 0
        else:
            logger.error("转换失败")
            return 1
            
    except Exception as e:
        logger.error(f"转换过程中出错: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
