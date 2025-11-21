package lab.aui.brand_service.command;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class CreateBrandCommand {
    private String name;
    private String country;
}